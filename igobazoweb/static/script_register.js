// 회원가입 유효성 검사
function check(){
	
	if(! $("input[name=id]").val()){
		alert("아이디를 입력해주세요");
		$("input[name=id]").focus();
		return false
	} else if (! $("input[name=passwd]").val() ){
		alert("비밀번호를 입력해주세요");
		$("input[name=passwd]").focus();
		return false
		
	} else if (! $("input[name=passwd1]").val() ){
		alert("확인을 위한 비밀번호를 입력하세요");
		$("input[name=passwd]").focus();
		return false
		
	}else if ( $("input[name=passwd]").val() != $("input[name=passwd1]").val() ){
		alert("비밀번호가 다릅니다.");
		$("input[name=passwd]").focus();
		return false
		
	}else if ($("input[name=ok]").val() == "0"){
		alert("아이디가 중복입니다.");
		return false
	} 
		
}

// 회원가입 닉네임 유효성 검사
function register(){
	if(! $("input[name=nickname]").val()){
		alert("닉네임을 입력해주세요");
		$("input[name=nickname]").focus();
		return false
		
	}else if ($("input[name=go]").val() == "0"){
		alert("닉네임이 중복입니다.");
		return false
	}
	
}

// 회원정보 비밀번호 수정 유효성 검사
function editpasswd(){
	if(! $("input[name=passwd2]").val()) {
	alert("새로운 비밀번호를 입력해 주세요.");
	return false
	}
}

function ageCalculator() {
    var userinput = document.getElementById("DOB").value;
    var dob = new Date(userinput);
    if(userinput==null || userinput=='') {
      document.getElementById("message").innerHTML = "**Choose a date please!";  
      return false; 
    } else {
    
    //calculate month difference from current date in time
    var month_diff = Date.now() - dob.getTime();
    
    //convert the calculated difference in date format
    var age_dt = new Date(month_diff); 
    
    //extract year from date    
    var year = age_dt.getUTCFullYear();
    
    //now calculate the age of the user
    var age = Math.abs(year - 1970);
    
    //display the calculated age
    registersform.ages.value=age;
    
    //return document.getElementById("age") = age;
             
    }
		
	for( var i=0; i<registersform.pg.length; i++ ) {
		if( registersform.pg[i].checked ) {
			registersform.pg[i] = "True";
		}
	}
}

// 로그인
function logincheck(){
	if(!$("input[name=id]").val() ) {
		alert("아이디를 입력하세요");
		$("input[name=id]").focus();
		return false;
	} else if(!$("input[name=passwd]").val() ){
		alert("비밀번호를 입력하세요");
		$("input[name=passwd]").focus();
		return false;
	}
}

// 탈퇴
function delcheck(){
	if(!$("input[name=passwd]").val() ) {
		alert("비밀번호를 입력하세요");
		$("input[name=id]").focus();
		return false;	
	}
}

//id 중복확인 Ajax
$(document).ready(
	function () {
		$("#id_result").html("&nbsp;아이디를 입력하세요" );
	}
);

function idverify(){
	$.ajax({
			url : "idverify",
			type : "POST",
			data : {
				"id" : $("input[name=id]").val()
			},
			dataType : "text",
			success : function (data) {
				if (data =="중복되는 아이디 입니다."){
					regf.ok.value="0"					
				} else if (data =="사용가능한 아이디입니다."){
					regf.ok.value="1"	
				}
				
				$("#id_result").html(data);
			},
			error : function () {}
		}
	);
}

$(document).ready(
	function () {
		$("#nick_result").html("&nbsp;닉네임을 입력하세요" );
	}
);

function nickverify(){
	$.ajax({
			url : "nickverify",
			type : "POST",
			data : {
				"nickname" : $("input[name=nickname]").val()
			},
			dataType : "text",
			success : function (data) {
				if (data =="중복되는 닉네임 입니다."){
					registersform.go.value="0"					
				} else if (data =="사용가능한 닉네임입니다."){
					registersform.go.value="1"	
				}
			
				$("#nick_result").html(data);
			},
			error : function () {}
		}
	);
}

