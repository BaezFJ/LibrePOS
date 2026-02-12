const STATIC_CACHE_NAME = 'static-cache-v4';
const DYNAMIC_CACHE_NAME = 'dynamic-cache-v1';
const DYNAMIC_CACHE_LIMIT = 50;

const STATIC_ASSETS = [
    '/',
    '/static/css/variables.css',
    '/static/css/main.css',
    '/static/css/utilities.css',
    '/static/js/app.js',
    '/static/js/utils.js',
    '/static/manifest.json',
    '/static/img/icons/icon-72x72.png',
    '/static/img/icons/icon-96x96.png',
    '/static/img/icons/icon-128x128.png',
    '/static/img/icons/icon-144x144.png',
    '/static/img/icons/icon-152x152.png',
    '/static/img/icons/icon-192x192.png',
    '/static/img/icons/icon-384x384.png',
    '/static/img/icons/icon-512x512.png',
    '/static/vendor/beercss/beer.min.css',
    '/static/vendor/beercss/beer.min.js',
    '/static/vendor/google/css/material-symbols-rounded.css',
    '/static/vendor/google/fonts/material-symbols-rounded.woff2'
];

// Cache size limit function - recursively deletes oldest entries
const limitCacheSize = (cacheName, maxSize) => {
    caches.open(cacheName).then(cache => {
        cache.keys().then(keys => {
            if (keys.length > maxSize) {
                cache.delete(keys[0]).then(() => limitCacheSize(cacheName, maxSize));
            }
        });
    });
};

// Install service worker
self.addEventListener('install', event => {
    console.log('[Service Worker] Installing...');
    self.skipWaiting();
    event.waitUntil(
        caches.open(STATIC_CACHE_NAME).then(cache => {
            console.log('[Service Worker] Pre-caching app shell');
            return cache.addAll(STATIC_ASSETS);
        })
    );
});

// Activate event - clean up old caches
self.addEventListener('activate', event => {
    console.log('[Service Worker] Activating...');
    event.waitUntil(
        caches.keys().then(keys => {
            return Promise.all(
                keys
                    .filter(key => key !== STATIC_CACHE_NAME && key !== DYNAMIC_CACHE_NAME)
                    .map(key => {
                        console.log('[Service Worker] Deleting old cache:', key);
                        return caches.delete(key);
                    })
            );
        }).then(() => {
            console.log('[Service Worker] Claiming clients');
            return self.clients.claim();
        })
    );
});

// Fetch event - cache-first strategy with network fallback
self.addEventListener('fetch', event => {
    const request = event.request;

    // Skip non-GET requests
    if (request.method !== 'GET') {
        return;
    }

    // Skip cross-origin requests
    if (!request.url.startsWith(self.location.origin)) {
        return;
    }

    event.respondWith(
        caches.match(request).then(cachedResponse => {
            if (cachedResponse) {
                return cachedResponse;
            }

            return fetch(request).then(networkResponse => {
                // Only cache successful same-origin responses
                if (!networkResponse || networkResponse.status !== 200 || networkResponse.type !== 'basic') {
                    return networkResponse;
                }

                // Clone response before caching
                const responseToCache = networkResponse.clone();
                caches.open(DYNAMIC_CACHE_NAME).then(cache => {
                    cache.put(request, responseToCache);
                    limitCacheSize(DYNAMIC_CACHE_NAME, DYNAMIC_CACHE_LIMIT);
                });

                return networkResponse;
            });
        }).catch(() => {
            // Navigation requests with no cache - let browser handle
            return;
        })
    );
});

// Message event - handle cache clearing from main thread
self.addEventListener('message', event => {
    if (event.data && event.data.type === 'CLEAR_CACHES') {
        console.log('[Service Worker] Clearing all caches...');
        event.waitUntil(
            caches.keys().then(cacheNames => {
                return Promise.all(
                    cacheNames.map(cacheName => caches.delete(cacheName))
                );
            }).then(() => {
                console.log('[Service Worker] All caches cleared');
                // Notify the client that caches are cleared
                if (event.ports && event.ports[0]) {
                    event.ports[0].postMessage({ type: 'CACHES_CLEARED' });
                }
            })
        );
    }

    if (event.data && event.data.type === 'SKIP_WAITING') {
        self.skipWaiting();
    }
});
