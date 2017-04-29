function checkPass(){
  var pass1 = document.getElementById("inputPassword3").value;
  var pass2 = document.getElementById("inputPassword4").value;
  var l1=pass1.length;
  var l2=pass2.length;

  if(l1>=8)
  {
    if(pass1!=pass2)
    {
      alert("Please enter the same password");
      return false;
    }
    else
    {
      return true;
    }
   }
   else
   {
     alert("Password too short");
     return false;
   }
}
