function logoutUser() {
    document.getElementById("username").value = "";
    document.getElementById("email").value = "";
    document.getElementById("nickname").value = "";
    document.getElementById("logout-form").submit();
  }