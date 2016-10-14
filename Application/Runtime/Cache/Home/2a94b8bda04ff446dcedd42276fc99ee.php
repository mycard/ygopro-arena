<?php if (!defined('THINK_PATH')) exit();?><html>
<head>
<meta char="utf8" />
<title><?php echo ($web_title); ?></title>
</head>
<body>
	<form action="./index.php?c=trueskill" method="post">
		<input type="input" name="usernameA"/>
		<input type="input" name="usernameB"/>
		<input type="input" name="userscoreA"/>
		<input type="input" name="userscoreB"/>
		<input type="hidden" name="accesskey" value="R6R0ahhut744Ni2NX2oDEi15pRUXDQAu" />
		<input type="hidden" name="arena" value="athletic" />
		<input type="submit" />
	</form>
	<br>
	<form action="../index.php?c=query" method="get">
		<input type="input" name="username"/>
		<input type="submit" />
	</form>
</body>
</html>