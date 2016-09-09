<?php

function Tureskill($A_u,$B_u,$A_o,$B_o,$usernameA,$usernameB){//清算历史积分
	
	$k = 32; //K越大越保守
	$A_u = $A_u + 5;
	$B_u = $B_u + 5;
	
	$A_o = $A_o + 5;
	$B_o = $B_o + 5;
	
	
	
	$EndResult = array(
		array(
			'name'=>$usernameA,
			'u'=>$A_u,
			'o'=>$A_o
		),
		array(
			'name'=>$usernameB,
			'u'=>$B_u,
			'o'=>$B_o
		)
	);
	
	return $EndResult;

}


function ClearingExp($A_exp,$B_exp,$usernameA,$usernameB){//清算历史积分
	
	$k = 32; //K越大越保守
	$A_exp = $A_exp;
	$B_exp = $B_exp + 5;
	
	
	
	$EndResult = array(
		array(
			'name'=>$usernameA,
			'exp'=>$A_exp
		),
		array(
			'name'=>$usernameB,
			'exp'=>$B_exp
		)
	);
	
	return $EndResult;

}


function QueryData($username){//查询用户数据
	$mysql = M("rating_index");//连接数据库
	$data = $mysql->where('username="'.$username.'"')->find();//查询某个用户的所有信息
	return $data;
}


function UpdataSkill($username,$o,$u,$games,$win,$lose,$last){//更新用户
	$mysql = M("rating_index");
	$data['games'] = $games; //总场数
	$data['win'] = $win; //总胜利
	$data['lose'] = $lose; //总失败
	$data['last'] = $last; //最后一场输赢
	$data['u'] = $u; //u
	$data['o'] = $o; //o
	$mysql->where('username="'.$username.'"')->save($data); //更新数据
	
}

function UpdataExp($username,$exp,$games,$win,$lose,$last){//更新用户
	$mysql = M("rating_index");
	$data['games'] = $games; //总场数
	$data['win'] = $win; //总胜利
	$data['lose'] = $lose; //总失败
	$data['last'] = $last; //最后一场输赢
	$data['exp'] = $exp; //exp
	$mysql->where('username="'.$username.'"')->save($data); //更新数据
	
}


function verifica($ak){//安全认证
	$mysql = M("safe_ak");
	$data = $mysql->where('ak="'.$ak.'"')->find();
	if($data == NULL){
		return 1;//没有该ak
	}elseif($data == false){
		return 2;//查询出错
	}else{
		return 0;//成功
	}
}


function CheckUser($username){//判断是否数据表中存在用户名
	$mysql = M("rating_index");//连接数据库
	$data = $mysql->where('username="'.$username.'"')->find();//查询某个用户的所有信息
	if($data == NULL){
		$new_data['username'] = $username;
		$mysql->data($new_data)->add();
	}
}

?>