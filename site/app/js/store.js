/*
 * Capa de datos de Fiestalia.
 * Dos implementaciones con la misma interfaz:
 *   - LocalStore    → IndexedDB del navegador (modo demo, sin servidor)
 *   - SupabaseStore → Supabase (Postgres + Storage)
 * window.store se elige en función de FIESTALIA_CONFIG.
 *
 * Interfaz:
 *   createAlbum(data) → { album, adminKey }
 *   getAlbum(code) → album | null
 *   getAlbumAdmin(code, adminKey) → album (lanza si la clave no es válida)
 *   updateAlbum(code, adminKey, patch) → album
 *   listPhotos(code, { includeHidden }) → [photo]
 *   addPhoto(code, { file, thumbBlob, uploader, width, height }) → photo
 *   setPhotoHidden(code, adminKey, photoId, hidden)
 *   deletePhoto(code, adminKey, photoId)
 *   photoUrl(photo) / thumbUrl(photo) → URL para <img>/<video>
 *   fetchBlob(photo) → Blob (para el ZIP)
 *   subscribe(code, cb) → unsubscribe()   (nuevas fotos en tiempo real)
 *   applyPayment(code, adminKey, planId) → album   (solo demo)
 */
(function () {
  const CFG = window.FIESTALIA_CONFIG || {};
  const B = window.BRAND || {};
  const PLANS = (B.plans || []).reduce((m, p) => (m[p.id] = p, m), {});

  const rand = (n) => {
    const chars = "abcdefghjkmnpqrstuvwxyz23456789";
    const a = new Uint8Array(n); crypto.getRandomValues(a);
    return Array.from(a, (x) => chars[x % chars.length]).join("");
  };
  const uuid = () => (crypto.randomUUID ? crypto.randomUUID() : rand(24));
  async function sha256(s) {
    const buf = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(s));
    return Array.from(new Uint8Array(buf), (b) => b.toString(16).padStart(2, "0")).join("");
  }
  function planFor(id) { return PLANS[id] || PLANS.gratis || { id: "gratis", photos: 50, months: 1, liveWall: false }; }
  function expiresAt(planId, from) {
    const d = new Date(from || Date.now()); d.setMonth(d.getMonth() + (planFor(planId).months || 1)); return d.toISOString();
  }
  function newAlbumRecord(data, adminKeyHash) {
    const plan = data.plan && PLANS[data.plan] ? data.plan : "gratis";
    const now = new Date().toISOString();
    return {
      code: rand(8),
      admin_key_hash: adminKeyHash,
      name: data.name.trim(),
      event_date: data.date || null,
      event_type: data.type || "boda",
      organizer_name: data.organizer.trim(),
      organizer_email: data.email.trim().toLowerCase(),
      welcome: (data.welcome || "").trim(),
      plan: "gratis",                 // el plan de pago se activa tras el pago
      requested_plan: plan,
      photo_limit: planFor("gratis").photos,
      uploads_open: true,
      moderation: !!data.moderation,  // ocultar fotos nuevas hasta aprobarlas
      selfie_enabled: false,
      created_at: now,
      expires_at: expiresAt("gratis", now)
    };
  }

  /* ───────────────────────── LocalStore (IndexedDB) ───────────────────────── */
  class LocalStore {
    constructor() { this.mode = "demo"; this._db = null; this._subs = {}; this._urls = new Map(); }
    db() {
      if (this._db) return Promise.resolve(this._db);
      return new Promise((res, rej) => {
        const req = indexedDB.open("fiestalia-demo", 1);
        req.onupgradeneeded = () => {
          const d = req.result;
          d.createObjectStore("albums", { keyPath: "code" });
          const p = d.createObjectStore("photos", { keyPath: "id" });
          p.createIndex("album", "album_code");
          d.createObjectStore("blobs", { keyPath: "id" });
        };
        req.onsuccess = () => { this._db = req.result; res(this._db); };
        req.onerror = () => rej(req.error);
      });
    }
    tx(stores, mode, fn) {
      return this.db().then((d) => new Promise((res, rej) => {
        const t = d.transaction(stores, mode); const out = fn(t);
        t.oncomplete = () => res(out && out.result !== undefined ? out.result : out);
        t.onerror = () => rej(t.error); t.onabort = () => rej(t.error);
      }));
    }
    get(store, key) { return this.db().then((d) => new Promise((res, rej) => { const r = d.transaction(store).objectStore(store).get(key); r.onsuccess = () => res(r.result || null); r.onerror = () => rej(r.error); })); }
    put(store, val) { return this.tx(store, "readwrite", (t) => t.objectStore(store).put(val)); }
    del(store, key) { return this.tx(store, "readwrite", (t) => t.objectStore(store).delete(key)); }

    async createAlbum(data) {
      const adminKey = rand(20);
      const album = newAlbumRecord(data, await sha256(adminKey));
      await this.put("albums", album);
      return { album: this._pub(album), adminKey };
    }
    _pub(a) { if (!a) return null; const { admin_key_hash, ...rest } = a; return rest; }
    async getAlbum(code) { return this._pub(await this.get("albums", code)); }
    async getAlbumAdmin(code, adminKey) {
      const a = await this.get("albums", code);
      if (!a) throw new Error("Álbum no encontrado");
      if (a.admin_key_hash !== await sha256(adminKey || "")) throw new Error("Clave de administración no válida");
      return this._pub(a);
    }
    async updateAlbum(code, adminKey, patch) {
      await this.getAlbumAdmin(code, adminKey);
      const a = await this.get("albums", code);
      const allowed = ["name", "event_date", "welcome", "uploads_open", "moderation", "selfie_enabled"];
      allowed.forEach((k) => { if (k in patch) a[k] = patch[k]; });
      await this.put("albums", a); return this._pub(a);
    }
    async applyPayment(code, adminKey, planId) {
      await this.getAlbumAdmin(code, adminKey);
      const a = await this.get("albums", code); const p = planFor(planId);
      a.plan = p.id; a.photo_limit = p.photos; a.paid_at = new Date().toISOString(); a.expires_at = expiresAt(p.id, a.paid_at);
      await this.put("albums", a); return this._pub(a);
    }
    async listPhotos(code, opts = {}) {
      const d = await this.db();
      const all = await new Promise((res, rej) => { const r = d.transaction("photos").objectStore("photos").index("album").getAll(code); r.onsuccess = () => res(r.result || []); r.onerror = () => rej(r.error); });
      return all.filter((p) => opts.includeHidden || !p.hidden).sort((x, y) => (x.created_at < y.created_at ? 1 : -1));
    }
    async countPhotos(code) { return (await this.listPhotos(code, { includeHidden: true })).length; }
    async addPhoto(code, { file, thumbBlob, uploader, width, height, duration }) {
      const a = await this.get("albums", code);
      if (!a) throw new Error("Álbum no encontrado");
      if (!a.uploads_open) throw new Error("El organizador ha cerrado las subidas");
      if ((await this.countPhotos(code)) >= a.photo_limit) throw Object.assign(new Error("limit"), { code: "LIMIT" });
      const id = uuid();
      const photo = { id, album_code: code, uploader_name: uploader || "Invitado", type: file.type.startsWith("video") ? "video" : "image", mime: file.type, size: file.size, width: width || null, height: height || null, duration: duration || null, hidden: !!a.moderation, created_at: new Date().toISOString(), storage_path: "local:" + id };
      await this.put("blobs", { id, file, thumb: thumbBlob || null });
      await this.put("photos", photo);
      (this._subs[code] || []).forEach((cb) => cb(photo));
      return photo;
    }
    async setPhotoHidden(code, adminKey, photoId, hidden) {
      await this.getAlbumAdmin(code, adminKey);
      const p = await this.get("photos", photoId); if (!p) return; p.hidden = !!hidden; await this.put("photos", p); return p;
    }
    async deletePhoto(code, adminKey, photoId) {
      await this.getAlbumAdmin(code, adminKey);
      await this.del("photos", photoId); await this.del("blobs", photoId);
      const u = this._urls.get(photoId); if (u) { URL.revokeObjectURL(u.full); URL.revokeObjectURL(u.thumb); this._urls.delete(photoId); }
    }
    async _urlsFor(photo) {
      if (this._urls.has(photo.id)) return this._urls.get(photo.id);
      const b = await this.get("blobs", photo.id);
      const full = b ? URL.createObjectURL(b.file) : "";
      const thumb = b && b.thumb ? URL.createObjectURL(b.thumb) : full;
      const u = { full, thumb }; this._urls.set(photo.id, u); return u;
    }
    async photoUrl(photo) { return (await this._urlsFor(photo)).full; }
    async thumbUrl(photo) { return (await this._urlsFor(photo)).thumb; }
    async fetchBlob(photo) { const b = await this.get("blobs", photo.id); return b ? b.file : null; }
    subscribe(code, cb) {
      (this._subs[code] = this._subs[code] || []).push(cb);
      // Cambios desde otras pestañas del mismo navegador
      const bc = ("BroadcastChannel" in window) ? new BroadcastChannel("fiestalia-" + code) : null;
      if (bc) bc.onmessage = (e) => cb(e.data);
      const orig = cb; const wrapped = (p) => { if (bc) bc.postMessage(p); };
      this._subs[code].push(wrapped);
      return () => { this._subs[code] = (this._subs[code] || []).filter((f) => f !== orig && f !== wrapped); if (bc) bc.close(); };
    }
  }

  /* ───────────────────────── SupabaseStore ───────────────────────── */
  class SupabaseStore {
    constructor(url, key) {
      this.mode = "supabase";
      this.sb = window.supabase.createClient(url, key);
      this.bucket = CFG.storageBucket || "media";
    }
    async createAlbum(data) {
      const adminKey = rand(20);
      const rec = newAlbumRecord(data, await sha256(adminKey));
      // Sin .select(): la tabla albums no es legible directamente (RLS); ya tenemos todos los datos en rec
      const { error } = await this.sb.from("albums").insert(rec);
      if (error) throw error;
      return { album: this._pub(rec), adminKey };
    }
    _pub(a) { if (!a) return null; const { admin_key_hash, ...rest } = a; return rest; }
    async getAlbum(code) {
      const { data, error } = await this.sb.from("albums_public").select("*").eq("code", code).maybeSingle();
      if (error) throw error; return data;
    }
    async getAlbumAdmin(code, adminKey) {
      const { data, error } = await this.sb.rpc("album_admin", { p_code: code, p_key: adminKey || "" });
      if (error) throw error; if (!data) throw new Error("Clave de administración no válida"); return data;
    }
    async updateAlbum(code, adminKey, patch) {
      const { data, error } = await this.sb.rpc("album_update", { p_code: code, p_key: adminKey, p_patch: patch });
      if (error) throw error; return data;
    }
    async applyPayment() { throw new Error("El pago se confirma automáticamente desde Stripe. Si ya has pagado, recarga la página en unos segundos."); }
    async listPhotos(code, opts = {}) {
      let q = this.sb.from("photos").select("*").eq("album_code", code).order("created_at", { ascending: false });
      if (!opts.includeHidden) q = q.eq("hidden", false);
      const { data, error } = await q; if (error) throw error; return data || [];
    }
    async addPhoto(code, { file, thumbBlob, uploader, width, height, duration }) {
      const id = uuid();
      const ext = (file.name.split(".").pop() || "bin").toLowerCase().replace(/[^a-z0-9]/g, "").slice(0, 5);
      const path = `${code}/${id}.${ext}`;
      const thumbPath = thumbBlob ? `${code}/${id}_t.jpg` : null;
      const up = await this.sb.storage.from(this.bucket).upload(path, file, { contentType: file.type, upsert: false });
      if (up.error) throw up.error;
      if (thumbBlob) { const t = await this.sb.storage.from(this.bucket).upload(thumbPath, thumbBlob, { contentType: "image/jpeg" }); if (t.error) throw t.error; }
      const { data, error } = await this.sb.rpc("photo_add", {
        p_id: id, p_code: code, p_uploader: uploader || "Invitado", p_type: file.type.startsWith("video") ? "video" : "image",
        p_mime: file.type, p_size: file.size, p_width: width || null, p_height: height || null, p_duration: duration || null,
        p_path: path, p_thumb: thumbPath
      });
      if (error) {
        await this.sb.storage.from(this.bucket).remove([path].concat(thumbPath ? [thumbPath] : []));
        if (String(error.message || "").includes("LIMIT")) throw Object.assign(new Error("limit"), { code: "LIMIT" });
        throw error;
      }
      return data;
    }
    async setPhotoHidden(code, adminKey, photoId, hidden) {
      const { error } = await this.sb.rpc("photo_set_hidden", { p_code: code, p_key: adminKey, p_id: photoId, p_hidden: !!hidden }); if (error) throw error;
    }
    async deletePhoto(code, adminKey, photoId) {
      const { data, error } = await this.sb.rpc("photo_delete", { p_code: code, p_key: adminKey, p_id: photoId }); if (error) throw error;
      if (data && data.length) await this.sb.storage.from(this.bucket).remove(data);
    }
    _url(path) { return this.sb.storage.from(this.bucket).getPublicUrl(path).data.publicUrl; }
    async photoUrl(photo) { return this._url(photo.storage_path); }
    async thumbUrl(photo) { return this._url(photo.thumb_path || photo.storage_path); }
    async fetchBlob(photo) { const r = await fetch(this._url(photo.storage_path)); return r.ok ? r.blob() : null; }
    subscribe(code, cb) {
      const ch = this.sb.channel("album-" + code)
        .on("postgres_changes", { event: "INSERT", schema: "public", table: "photos", filter: `album_code=eq.${code}` }, (p) => cb(p.new))
        .subscribe();
      return () => this.sb.removeChannel(ch);
    }
  }

  window.store = (CFG.supabaseUrl && CFG.supabaseAnonKey && window.supabase)
    ? new SupabaseStore(CFG.supabaseUrl, CFG.supabaseAnonKey)
    : new LocalStore();
  window.store.planFor = planFor;
  window.store.PLANS = PLANS;
})();
