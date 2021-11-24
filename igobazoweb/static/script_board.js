$(document).ready(
	function() {
		
	
	}
);

// 글쓰기
function writecheck() {
	writer = $("input[name=writer]").val();
	subject = $("input[name=subject]").val();
	content = $("textarea").val();
	passwd2 = $("input[name=passwd2]").val();

	//movie_subject = $("input[name=movie_subject]").val();
	//movie_num = $("input[name=movie_num]").val();	

	if( ! writer ) {
		alert( "작성자를 입력하세요" );
		$("input[name=writer]" ).focus();
		return false;
	} else if( ! subject ) {
		alert( "제목을 입력하세요" );
		$("input[name=subject]" ).focus();
		return false;
	} else if( ! content ) {
		alert( "내용을 입력하세요" );
		$("textarea").focus();
		return false;
	} else if( ! passwd2 ) {
		alert( "비밀번호를 입력하세요" );
		$("input[name=passwd2]").focus();
		return false;
	} 
	//else if( ! movie_subject ) {
	//	alert( "영화 제목을 입력하세요" );
	//	$("input[name=movie_subject]").focus();
	//	return false;
	//} else if( ! movie_num ) {
	//	alert( "일련번호를 입력하세요" );
	//	$("input[name=movie_num]").focus();
	//	return false;
	//}

}

	
	
	
	
	
	
	