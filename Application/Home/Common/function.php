<?php

/* function Tureskill($A_u,$B_u,$A_o,$B_o,$usernameA,$usernameB){//清算历史积分
	
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

} */


function ClearingRating($ratingA,$ratingB,$resultA,$resultB,$usernameA,$usernameB){//������ʷ����
	$weight = 32;
	
	$differA = $ratingB - $ratingA; 
	$differB = $ratingA - $ratingB; 
	
	$Ea = 1/(1+(10^$differA)/400);
	$Eb = 1/(1+(10^$differB)/400); 

	if($Ea <= 0){
		$Ea = 1 - $Eb;
	}elseif($Ea >0){
		$Eb = 1 - $Ea;
	}
	$EndRatingA = round($ratingA + $weight * ($resultA - $Ea),4); 
	
	$EndRatingB = round($ratingB + $weight * ($resultB - $Eb),4);
	
	$EndResult = array(
		array(
			'name'=>$usernameA,
			'pt'=>$EndRatingA
		),
		array(
			'name'=>$usernameB,
			'pt'=>$EndRatingB
		)
	);
	
	return $EndResult;
}

function ClearingExp($A_exp,$B_exp,$usernameA,$usernameB,$draw){//清算历史积分

	if($draw != true){//非平局
		if($B_exp > $A_exp){
			$A_exp = $A_exp + 1;
			$B_exp = $B_exp + 1;
		}else{
			$A_exp = $A_exp + 1;
			$B_exp = $B_exp;
		}

	}else{//平局
		$A_exp += 1;
		$B_exp += 1;
	}

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
	$data = $mysql->where("username='".$username."'")->find();//查询某个用户的所有信息
	
	return $data;
}


/* function UpdataSkill($username,$o,$u,$games,$win,$lose,$last){//更新用户
	$mysql = M("rating_index");
	$data['game'] = $games; //总场数
	$data['win'] = $win; //总胜利
	$data['lose'] = $lose; //总失败
	$data['last'] = $last; //最后一场输赢
	$data['u'] = $u; //u
	$data['o'] = $o; //o
	$status = $mysql->where("username='".$username."'")->save($data); //更新数据
	if($status == false){
		error_return('500');
	}
} */


function UpdataElo($username,$pt,$games,$win,$lose,$last){//更新用户
	$mysql = M("rating_index");
	$data['pt'] = $pt; //pt 
	$data['game'] = $games; //总场数
	$data['win'] = $win; //总胜利
	$data['lose'] = $lose; //总失败
	$data['last'] = $last; //最后一场输赢 
	$status = $mysql->where("username='".$username."'")->save($data); //更新数据
	
	if($status == false){
		error_return('500');
	}
}

function UpdataExp($username,$exp,$games,$win,$lose,$last){//更新用户
	$mysql = M("rating_index");
	$data['game'] = $games; //总场数
	$data['win'] = $win; //总胜利
	$data['lose'] = $lose; //总失败
	$data['last'] = $last; //最后一场输赢
	$data['exp'] = $exp; //exp
	$status = $mysql->where("username='".$username."'")->save($data); //更新数据
	if($status == false){
		error_return('500');
	}
}


function verifica($ak){//安全认证
	$mysql = M("safe_ak");
	$data = $mysql->where("ak='".$ak."'")->find();
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
	$data = $mysql->where("username='".$username."'")->find();//查询某个用户的所有信息
	if($data == NULL){
        $new_data = array(
			'username' => $username,
            'exp' => '800',
            'pt' => '800',
            'win' => '0',
            'lose' => '0',
            'game' => '0',
            'status' => '0',
            'o' => '0',
            'u' => '0',
			'last' => '0'
        );
		$mysql->data($new_data)->add();
	}
}

function error_return($type){
	if($type == '500'){
		header('HTTP/1.1 500 Internal Server Error');
		exit;
	}elseif($type == '404'){
		header('HTTP/1.1 404 Not Found');
		exit;
	}
}

function exp_rank($username){
	$db = M("rating_index");//连接数据库
	$exp_numb = $db->where("username='".$username."'")->getField('exp');
	
	$exp_select = $db->where("exp>='".$exp_numb."'")->order("exp DESC,username ASC")->getField('username,exp');

	foreach ($exp_select as $k=>$v) {
		  if($k == $username){
			  	if($i == NULL){
					$i = 1;
					return $i;
				}else{
				return $i;
				}
			  }
			  
		  $i++;
	}

}

function arena_rank($username){
	$db = M("rating_index");//连接数据库
	$exp_numb = $db->where("username='".$username."'")->getField('pt');
	
	$exp_select = $db->where("pt>='".$exp_numb."'")->order("pt DESC,username ASC")->getField('username,pt');

	foreach ($exp_select as $k=>$v) {
		  if($k == $username){
			  return $i;
			  }
			  
		  $i++;
	}
	
}

function count_ratio($win,$lose){
	return round(($win/$lose)*100,2);
}




/*

function Trueskill_fun($player_A_o,$player_B_o,$player_A_u,$player_B_u,$player_A_pt,$player_B_pt){
	//player A is loser ; player B is winner;
	$k = 3;
	$player_A_o = 25 / $k ;
	$player_B_o = 25 / $k ;
	$player_A_u = 25;
	$player_B_u = 25;
	$player_A_pt = 25;
	$player_B_pt = 25;
	
	
	
	$t = $player_B_u - $player_A_u ; // t = u_winner - u_loser
	
	######################################################################
	
	$xba = ($player_A_pt + $player_B_pt) / 2 ;//平均数
	$alpha = pow(($player_B_pt - $xba),2) + pow(($player_A_pt - $xba),2);//方差	
	$beta =  sqrt($alpha);//标准差
	
	######################################################################
	
	$csqr = (2 * pow($beta,2)) + pow($player_B_o,2) + pow($player_A_o,2); // c^2 = 2*beta^2 + winner_o^2 + loser_o^2;
	
	######################################################################
	
	
	
	
	
	echo $beta;
	
}

*/





?>