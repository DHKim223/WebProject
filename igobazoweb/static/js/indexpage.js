$(document).ready(function(){
	$.ajax({
		url : "https://api.themoviedb.org/3/movie/popular?api_key=90d0e27636f760e0ce5b5d2a38c09a7a&language=ko-KR&region=KR",
		type : "GET",
		data : {},
		success : function(response){
			let datas = response['results'];
			let poster_url = "https://image.tmdb.org/t/p/original"
			for (let i=0; i<datas.length; i++){
				let adult = datas[i]['adult']
				let backdrop_path = datas[i]['backdrop_path']
				let genre_ids = datas[i]['genre_ids']
				let id = datas[i]['id']
				let original_language = datas[i]['original_language']
				let original_title = datas[i]['original_title']
				let overview = datas[i]['overview']
				let popularity = datas[i]['popularity']
				let poster_path = poster_url + datas[i]['poster_path']
				let release_date = datas[i]['release_date']
				let title = datas[i]['title']
				let video = datas[i]['video']
				let vote_average = datas[i]['vote_average']
				let vote_count = datas[i]['vote_count']
				let rank = i + 1
				
				let temp_html = `
					<div class="movie_box">
                      	<div class="poster">
                          	<img class="cursor" src="${poster_path}"  alt="${title}" onclick="location='detailpage?movieCd=${id}'">
                          	<div class="rank"><strong>${rank}</strong></div>
                      	</div>
                      	<div class="infor">
                        	<h3><strong><a href="detailpage?movieCd=${id}" >${title}</a></strong></h3>
                        	<h5><span>개봉일 : ${release_date}</span></h5>
                    	</div>
                  	</div>
              	`;
			
              	$("#movie_slide").append(temp_html)

			}
			
			$('.slide').slick({
				arrows : true,
				infinite : true,
				slidesToShow : 5,
				slidesToScroll : 5,
				autoplay : true,
				autoplaySpeed : 8000,
				responsive: [ 
					{  
						breakpoint: 960, //화면 사이즈 960px
						settings: {
							//위에 옵션이 디폴트 , 여기에 추가하면 그걸로 변경
							slidesToShow:4,
							slidesToScroll:4
						} 
					},
					{ 
						breakpoint: 768, //화면 사이즈 768px
						settings: {	
							//위에 옵션이 디폴트 , 여기에 추가하면 그걸로 변경
							slidesToShow:3,
							slidesToScroll:3
						} 
					},
					{ breakpoint: 600, // 화면 사이즈 600px
						settings: { 
							slidesToShow: 2, 
							slidesToScroll: 2 
						}
					},
					{ breakpoint: 320, // 화면 사이즈 320px
						settings: { 
							slidesToShow: 1, 
							slidesToScroll: 1 
						} 
					} 
				]
			});
		}
	});
	
	$.ajax({
		url : "https://api.themoviedb.org/3/movie/popular?api_key=90d0e27636f760e0ce5b5d2a38c09a7a&language=ko-KR&region=KR",
		type : "GET",
		data : {},
		success : function(response){
			let datas = response['results'];
			let poster_url = "https://image.tmdb.org/t/p/original"
			for (let i=0; i<datas.length; i++){
				let adult = datas[i]['adult']
				let backdrop_path = datas[i]['backdrop_path']
				let genre_ids = datas[i]['genre_ids']
				let id = datas[i]['id']
				let original_language = datas[i]['original_language']
				let original_title = datas[i]['original_title']
				let overview = datas[i]['overview']
				let popularity = datas[i]['popularity']
				let poster_path = poster_url + datas[i]['poster_path']
				let release_date = datas[i]['release_date']
				let title = datas[i]['title']
				let video = datas[i]['video']
				let vote_average = datas[i]['vote_average']
				let vote_count = datas[i]['vote_count']
				let rank = i + 1
				
				let temp_html = `
					<div class="movie_box">
                      	<div class="poster">
                          	<img class="cursor" src="${poster_path}"  alt="${title}" onclick="location='detailpage?movieCd=${id}'">
                          	<div class="rank"><strong>${rank}</strong></div>
                      	</div>
                      	<div class="infor">
                        	<h3><strong><a href="detailpage?movieCd=${id}" >${title}</a></strong></h3>
                        	<h5><span>개봉일 : ${release_date}</span></h5>
                    	</div>
                  	</div>
              	`;
			
              	$("#movie_slide").append(temp_html)

			}
		}
	});
});