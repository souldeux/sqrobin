$(document).ready(function(){
	$('[data-toggle="popover"]').popover({'html':true});

	$("#sun").click(function(){
		$("#mask").fadeTo(1000, 1, function(){
			$('#report').addClass('animated bounceOutLeft');
			$("body").css('background-image', 'url('+"{% static 'souldeux/planets/sun.jpg' %}"+')');
			$("#mask").fadeTo(2000, 0, function(){
				$("#report").html("<h1 class='page-header'>The Sun</h1>");
				$("#report").append("<p>high: 1.57 X 10<sup>7</sup> K | low: 5 X 10<sup>6</sup> K</p>");
				$("#report").append("<p>circumference: 4.379 X 10<sup>6</sup> km (109x Earth)</p>");
				$("#report").append("<p>volume: 1.41 X 10<sup>18</sup> km<sup>3</sup> (1,300,000x Earth)</p>");
				$("#report").append("<p>avg density: 1.408 g/cm<sup>3</sup> (0.255x Earth)</p>");
				$("#report").append("<p>surface gravity: 274.0 m/s<sup>2</sup> (28x Earth)</p>");
				$("#report").addClass('bounceInRight');
				$("#report").removeClass('bounceOutLeft');
				$("#report").css('background-color','rgba(0,0,0,0.4)');
			});
		});
	});
	$("#mercury").click(function(){
		$("#mask").fadeTo(1000, 1, function(){
			$('#report').addClass('animated bounceOutLeft');
			$("body").css('background-image', 'url('+"{% static 'souldeux/planets/mercury.jpg' %}"+')');
			$("#mask").fadeTo(2000, 0, function(){
				$("#report").html("<h1 class='page-header'>Mercury</h1>");
				$("#report").append("<p>high: 700 K | low: 80 K</p>");
				$("#report").append("<p>circumference: 15,329 km (0.38x Earth)</p>")
				$("#report").append("<p>volume: 6.083 X 10<sup>10</sup> km<sup>3</sup> (0.056x Earth)</p>");
				$("#report").append("<p>mass: 3.3011 X 10<sup>23</sup> kg (0.055x Earth)</p>");
				$("#report").append("<p>surface gravity: 3.7 m/s<sup>2</sup> (0.38x Earth)</p>");
				$("#report").addClass('bounceInRight');
				$("#report").removeClass('bounceOutLeft');
				$("#report").css('background-color','rgba(0,0,0,0.3)');
			});
		});
	});
	$("#venus").click(function(){
		$("#mask").fadeTo(1000, 1, function(){
			$('#report').addClass('animated bounceOutLeft');
			$("body").css('background-image', 'url('+"{% static 'souldeux/planets/venus.jpg' %}"+')');
			$("#mask").fadeTo(2000, 0, function(){
				$("#report").html("<h1 class='page-header'>Venus</h1>");
				$("#report").append("<p>avg temp: 737 K</p>");
				$("#report").append("<p>circumference: 38,025 km (0.949x Earth)</p>");
				$("#report").append("<p>volume: 9.2843 X 10<sup>11</sup> km<sup>3</sup> (0.866x Earth)</p>");
				$("#report").append("<p>mass: 4.8675 X 10<sup>24</sup> kg (0.815x Earth)</p>");
				$("#report").append("<p>surface gravity: 8.87 m/s<sup>2</sup> (0.904x Earth)</p>");
				$("#report").addClass('bounceInRight');
				$("#report").removeClass('bounceOutLeft');
				$("#report").css('background-color','rgba(0,0,0,0.4)');
			});
		});
	});
	$("#earth").click(function(){
		$("#mask").fadeTo(1000, 1, function(){
			$('#report').addClass('animated bounceOutLeft');
			$("body").css('background-image', 'url('+"{% static 'souldeux/planets/earth.jpg' %}"+')');
			$("#mask").fadeTo(2000, 0, function(){
				$("#report").html("<h1 class='page-header'>Earth</h1>");
				$("#report").append("<p>high: 330 K | low: 184 K</p>");
				$("#report").append("<p>circumference: 40,075 km</p>");
				$("#report").append("<p>volume: 1.083 X 10<sup>12</sup> km<sup>3</sup></p>");
				$("#report").append("<p>mass: 5.972 X 10<sup>24</sup> kg</p>");
				$("#report").append("<p>surface gravity: 9.807 m/s<sup>2</sup></p>");
				$("#report").addClass('bounceInRight');
				$("#report").removeClass('bounceOutLeft');
				$("#report").css('background-color','rgba(0,0,0,0.5)');
			});
		});
	});
	$("#mars").click(function(){
		$("#mask").fadeTo(1000, 1, function(){
			$('#report').addClass('animated bounceOutLeft');
			$("body").css('background-image', 'url('+"{% static 'souldeux/planets/mars.jpg' %}"+')');
			$("#mask").fadeTo(2000, 0, function(){
				$("#report").html("<h1 class='page-header'>Mars</h1>");
				$("#report").append("<p>high: 308 K | low: 130 K</p>");
				$("#report").append("<p>circumference: 21,344 km (0.533x Earth)</p>");
				$("#report").append("<p>volume: 1.6318 X 10<sup>11</sup> km<sup>3</sup> (0.151x Earth)</p>");
				$("#report").append("<p>mass: 6.4171 X 10<sup>23</sup> kg (0.107x Earth)</p>");
				$("#report").append("<p>surface gravity: 3.711 m/s<sup>2</sup> (0.376x Earth)</p>")
				$("#report").addClass('bounceInRight');
				$("#report").removeClass('bounceOutLeft');
				$("#report").css('background-color','rgba(0,0,0,0.6)');
			});
		});
	});
	$("#jupiter").click(function(){
		$("#mask").fadeTo(1000, 1, function(){
			$('#report').addClass('animated bounceOutLeft');
			$("body").css('background-image', 'url('+"{% static 'souldeux/planets/jupiter.jpg' %}"+')');
			$("#mask").fadeTo(2000, 0, function(){
				$("#report").html("<h1 class='page-header'>Jupiter</h1>");
				$("#report").append("<p>avg temp: 165 K</p>");
				$("#report").append("<p>circumference: 439,264 km (10.961x Earth)</p>");
				$("#report").append("<p>volume: 1.4313 X 10<sup>15</sup> km<sup>3</sup> (1321x Earth)</p>");
				$("#report").append("<p>mass: 1.8986 X 10<sup>27</sup> kg (317.8x Earth)</p>");
				$("#report").append("<p>surface gravity: 24.79 m/s<sup>2</sup> (2.528x Earth)")
				$("#report").addClass('bounceInRight');
				$("#report").removeClass('bounceOutLeft');
				$("#report").css('background-color','rgba(0,0,0,0.6)');
			});
		});
	});
	$("#saturn").click(function(){
		$("#mask").fadeTo(1000, 1, function(){
			$('#report').addClass('animated bounceOutLeft');
			$("body").css('background-image', 'url('+"{% static 'souldeux/planets/saturn.jpg' %}"+')');
			$("#mask").fadeTo(2000, 0, function(){
				$("#report").html("<h1 class='page-header'>Saturn</h1>");
				$("#report").append("<p>avg temp: 134 K</p>");
				$("#report").append("<p>circumference: 378,675 km (9.45x Earth)</p>");
				$("#report").append("<p>volume: 8.2713 X 10<sup>14</sup> km<sup>3</sup> (83.7x Earth)</p>");
				$("#report").append("<p>mass: 5.6836 X 10<sup>26</sup> kg (95.159x Earth)</p>");
				$("#report").append("<p>surface gravity: 10.44 m/s<sup>2</sup> (1.065x Earth)</p>");
				$("#report").addClass('bounceInRight');
				$("#report").removeClass('bounceOutLeft');
				$("#report").css('background-color','rgba(0,0,0,0)');
			});
		});
	});
	$("#uranus").click(function(){
		$("#mask").fadeTo(1000, 1, function(){
			$('#report').addClass('animated bounceOutLeft');
			$("body").css('background-image', 'url('+"{% static 'souldeux/planets/uranus.jpg' %}"+')');
			$("#mask").fadeTo(2000, 0, function(){
				$("#report").html("<h1 class='page-header'>Uranus</h1>");
				$("#report").append("<p>avg temp: 76 K</p>");
				$("#report").append("<p>circumference: 160,590 km (4x Earth)</p>");
				$("#report").append("<p>volume: 6.833 X 10<sup>13</sup> km<sup>3</sup>(63.086x Earth)</p>");
				$("#report").append("<p>mass: 8.6810 X 10<sup>25</sup> kg (14.536x Earth)</p>");
				$("#report").append("<p>surface gravity: 8.69 m/s<sup>2</sup> (0.886x Earth)")
				$("#report").addClass('bounceInRight');
				$("#report").removeClass('bounceOutLeft');
				$("#report").css('background-color','rgba(0,0,0,0.3)');
			});
		});
	});
	$("#neptune").click(function(){
		$("#mask").fadeTo(1000, 1, function(){
			$('#report').addClass('animated bounceOutLeft');
			$("body").css('background-image', 'url('+"{% static 'souldeux/planets/neptune.jpg' %}"+')');
			$("#mask").fadeTo(2000, 0, function(){
				$("#report").html("<h1 class='page-header'>Neptune</h1>");
				$("#report").append("<p>avg temp: 72 K</p>");
				$("#report").append("<p>circumference: 155,600 km (3.88x Earth)</p>");
				$("#report").append("<p>volume: 6.254 X 10<sup>13</sup> km<sup>3</sup> (57.54x Earth)</p>");
				$("#report").append("<p>mass: 1.0243 X 10<sup>26</sup> kg (17.147x Earth)</p>");
				$("#report").append("<p>surface gravity: 11.15 m/s<sup>2</sup> (1.14x Earth)</p>");
				$("#report").addClass('bounceInRight');
				$("#report").removeClass('bounceOutLeft');
				$("#report").css('background-color','rgba(0,0,0,0.3)');
			});
		});
	});

});