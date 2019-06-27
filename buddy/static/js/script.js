
// Facebook oAuth
var finished_rendering = function() {
    console.log("finished rendering plugins");
    var spinner = document.getElementById("spinner");
    spinner.removeAttribute("style");
    spinner.removeChild(spinner.childNodes[0]);
  }
  FB.Event.subscribe('xfbml.render', finished_rendering);

  window.fbAsyncInit = function () {
    FB.init({
        appId: '2424876137602826',
        autoLogAppEvents: true,
        xfbml: true,
        status: true,
        version: 'v3.3'
    });
    FB.Event.subscribe('auth.login', function () {
        window.location = '/welcome';
    });
};
FB.Event.subscribe('auth.logout', function () {
    window.location.href = '/';
});

// Google OAuth

  function onSignIn(googleUser) {
    // Useful data for your client-side scripts:
    var profile = googleUser.getBasicProfile();
    console.log("ID: " + profile.getId()); // Don't send this directly to your server!
    console.log('Full Name: ' + profile.getName());
    console.log('Given Name: ' + profile.getGivenName());
    console.log('Family Name: ' + profile.getFamilyName());
    console.log("Image URL: " + profile.getImageUrl());
    console.log("Email: " + profile.getEmail());

    // The ID token you need to pass to your backend:
    var id_token = googleUser.getAuthResponse().id_token;
    console.log("ID Token: " + id_token);
}