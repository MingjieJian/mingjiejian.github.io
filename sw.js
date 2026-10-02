// The old site installed a precaching service worker. This replacement clears every cache it
// created and unregisters itself, so returning visitors get the current pages from the network.
// Nothing registers a service worker any more (service-worker: false in _config.yml).
self.addEventListener("install", () => self.skipWaiting());
self.addEventListener("activate", event => {
  event.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.map(k => caches.delete(k))))
      .then(() => self.registration.unregister())
  );
});
