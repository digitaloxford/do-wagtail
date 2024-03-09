// Do things once everything has loaded in
window.addEventListener('load', function () {
    // Remove no-js class
    let element = document.getElementsByTagName("html");
    element[0].classList.remove("no-js");
});

// Thanks to Jeremy Keith's Going Offline book for making this so easy to get my head around.
// https://adactio.com/journal/13789

// Register our service worker.
// We place it in the root so it's scoped to the whole site and
// we don't have to deal with Service-Worker-Allowed headers
if (navigator.serviceWorker) {
    navigator.serviceWorker.register('/serviceworker.js')
        .then(function(registration) {
            console.log('Success!', registration.scope);
        })
        .catch(function(error) {
            console.error('Failure!', error);
        });
}
