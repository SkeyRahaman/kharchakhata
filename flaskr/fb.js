<script>
  window.fbAsyncInit = function() {
    FB.init({
      appId      : '253088142772668',
      cookie     : true,
      xfbml      : true,
      version    : 'v7.0'
    });
      
    FB.AppEvents.logPageView();   
      
  };

  (function(d, s, id){
     var js, fjs = d.getElementsByTagName(s)[0];
     if (d.getElementById(id)) {return;}
     js = d.createElement(s); js.id = id;
     js.src = "https://connect.facebook.net/en_US/sdk.js";
     fjs.parentNode.insertBefore(js, fjs);
   }(document, 'script', 'facebook-jssdk'));

  FB.getLoginStatus(function(response) {
      statusChangeCallback(response);
  });

  function checkLoginState() {
    FB.getLoginStatus(function(response) {
      statusChangeCallback(response);
    });
  }
  const statusChangeCallback = (response) =>{
    if (response.status === 'connected') {
      console.log(response.authResponse.accessToken);
    }
  };
</script>

<div class="text-center ml-0" id="google_api">
  <a href="/google_login" >
    <fb:login-button 
      scope="public_profile,email"
      onlogin="checkLoginState();">
    </fb:login-button>
  </a>
</div><br>