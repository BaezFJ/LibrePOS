const staticCacheName = 'static-cache-v2';
const dynamicCacheName = 'dynamic-cache-v1';
const staticAssets = [
    '/',
    '/offline.html',
    '/static/css/override.min.css',
    '/static/css/theme.min.css',
    '/static/css/style.min.css',
    '/static/js/app.js',
    '/static/js/ui.js',
    '/static/js/theme-switcher.js',
    '/static/manifest.json',
    '/static/images/icons/icon-72x72.png',
    '/static/images/icons/icon-96x96.png',
    '/static/images/icons/icon-128x128.png',
    '/static/images/icons/icon-144x144.png',
    '/static/images/icons/icon-152x152.png',
    '/static/images/icons/icon-192x192.png',
    '/static/images/icons/icon-384x384.png',
    '/static/images/icons/icon-512x512.png',
];

// Cache size limit function
const limitCacheSize = (cacheName, size) => {
    caches.open(cacheName).then(cache => {
        cache.keys().then(keys => {
            if (keys.length > size) {
                cache.delete(keys[0]).then(limitCacheSize(cacheName, size));
            }
        })
    })
};

// Install service worker
self.addEventListener('install', installEvent => {
    console.log('[Service Worker] Installing service worker...');
    skipWaiting();
    installEvent.waitUntil(
        caches.open(staticCacheName)
            .then(function (staticCache) {
                console.log('[Service Worker] Pre-caching app shell');
                return staticCache.addAll(staticAssets)
            })
    );
});

// Activate Event
self.addEventListener('activate', activateEvent => {
    // console.log('Service worker activated');
    activateEvent.waitUntil(
        caches.keys().then(keys => {
            // console.log(keys); // testing
            return Promise.all(keys
                .filter(key => key !== staticCacheName && key !== dynamicCacheName)
                .map(key => caches.delete(key))
            )
        })
    );
});

// Fetch Event
self.addEventListener('fetch', fetchEvent => {
    // console.log('Fetch event');
    fetchEvent.respondWith(
        caches.match(fetchEvent.request).then(cachedResponse => {
            return cachedResponse || fetch(fetchEvent.request).then(fetchResponse => {
                return caches.open(dynamicCacheName).then(dynamicCache => {
                    dynamicCache.put(fetchEvent.request.url, fetchResponse.clone());
                    limitCacheSize(dynamicCacheName, 10);
                    return fetchResponse;
                })
            });
        }).catch(() => {
            if (fetchEvent.request.url.indexOf('.html') > -1) {
                return caches.match('/offline.html');
            }
        })
    );
});