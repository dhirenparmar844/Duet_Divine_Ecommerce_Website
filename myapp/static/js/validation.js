function checkFname()
		{
			var f=document.frm.fname.value;
			var reg=/^[A-Za-z]+$/;
			if(f=="")
			{
				document.getElementById("fname").innerHTML="Please Enter First Name";
			}
			else if(!reg.test(f))
			{
				document.getElementById("fname").innerHTML="Please Enter Only Alphabets";
			}
			else
			{
				document.getElementById("fname").innerHTML="";	
			}
		}
		function checkEmail()
		{
			var e=document.frm.email.value;
			var reg=/^[A-Za-z0-9-_.]+@[A-Za-z]+\.+[A-Za-z]{2,4}$/;
			if(e=="")
			{
				document.getElementById("email").innerHTML="Please Enter Email";
			}
			else if(!reg.test(e))
			{
				document.getElementById("email").innerHTML="Please Enter Valid Email ID";	
			}
			else
			{
				document.getElementById("email").innerHTML="";	
			}
		}
		function checkMobile()
		{
			var m=document.frm.mobile.value;
			var reg=/^\d{10}$/;
			if(m=="")
			{
				document.getElementById("mobile").innerHTML="Please Enter Mobile";
			}
			else if(!reg.test(m))
			{
				document.getElementById("mobile").innerHTML="Please Enter 10 Digits Only";	
			}
			else
			{
				document.getElementById("mobile").innerHTML="";
			}
		}
		function checkPassword()
		{
			var p=document.frm.password.value;
			var reg=/^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[^a-zA-Z0-9])(?!.*\s).{8,15}$/;
			if(p=="")
			{
				document.getElementById("password").innerHTML="Please Enter Password";
			}
			else if(!reg.test(p))
			{
				document.getElementById("password").innerHTML="Min 1 Digit, Upper, Lower, Special(8,15)";
			}
			else
			{
				document.getElementById("password").innerHTML="";
			}
		}
		function checkCpassword()
		{
			var p1=document.frm.password.value;
			var p2=document.frm.cpassword.value;
			
			if(p2=="")
			{
				document.getElementById("cpassword").innerHTML="Please Enter Confirm Password";
			}
			else if(p1!=p2)
			{
				document.getElementById("cpassword").innerHTML="Password & Confirm Password Does Not Matched";
			}
			else
			{
				document.getElementById("cpassword").innerHTML="";
			}
		}