<html>
<head>
	<title>Hello World</title>
	<link rel="stylesheet" href="./static/styles.css">
	<link rel="stylesheet" href="./static/sam.css">
</head>
<body>
<nav>
	<ul>
		% for item in md:
		<li><a href="/{{item}}">{{item}}</a></li>
		% end 
	</ul>
</nav>
<div class="markdown-body">
{{!info}}
</div>
</body>
</html>
