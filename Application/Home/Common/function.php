<?php

function Tureskill($A_u,$B_u,$A_o,$B_o,$usernameA,$usernameB){//������ʷ����
	
	$k = 32; //KԽ��Խ����
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

function ClearingExp($A_exp,$B_exp,$usernameA,$usernameB){//������ʷ����
	
	$k = 32; //KԽ��Խ����
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

	$weight = 32; //Ȩֵ����Ϸ�Ѷ�Խ��ȨֵԽС
	
	$differA = $ratingB - $ratingA; //����������A��ֵ
	$differB = $ratingA - $ratingB; //����������B��ֵ
	
	
	$Ea = 1/(1+(10^$differA)/400); //��������A�������÷�
	$Eb = 1/(1+(10^$differB)/400); //��������B�������÷�
	
	if($Ea <= 0){
		$Ea = 1 - $Eb;
	}elseif($Ea >0){
		$Eb = 1 - $Ea;
	}

	$EndRatingA = $ratingA + $weight * ($resultA - $Ea); //��������A��Ϸ������Ļ���
	
	$EndRatingB = $ratingB + $weight * ($resultB - $Eb); //��������B��Ϸ������Ļ���
	
	$EndRatingResult = array(
		array(
			'name'=>$usernameA,
			'rating'=>$EndRatingA
		),
		array(
			'name'=>$usernameB,
			'rating'=>$EndRatingB
		)
	);
	
	return $EndRatingResult;
}
function QueryData($username){//��ѯ�û�����
	$mysql = M("rating_index");//�������ݿ�
	$data = $mysql->where('username="'.$username.'"')->find();//��ѯĳ���û���������Ϣ
	return $data;
}

function UpdataSkill($username,$o,$u,$games,$win,$lose,$last){//�����û�
	$mysql = M("rating_index");
	$data['games'] = $games; //�ܳ���
	$data['win'] = $win; //��ʤ��
	$data['lose'] = $lose; //��ʧ��
	$data['last'] = $last; //���һ����Ӯ
	$data['u'] = $u; //u
	$data['o'] = $o; //o
	$mysql->where('username="'.$username.'"')->save($data); //��������
	
}

function UpdataExp($username,$exp,$games,$win,$lose,$last){//�����û�
	$mysql = M("rating_index");
	$data['games'] = $games; //�ܳ���
	$data['win'] = $win; //��ʤ��
	$data['lose'] = $lose; //��ʧ��
	$data['last'] = $last; //���һ����Ӯ
	$data['exp'] = $exp; //exp
	$mysql->where('username="'.$username.'"')->save($data); //��������
	
}

function verifica($ak){//��ȫ��֤
	$mysql = M("safe_ak");
	$data = $mysql->where('ak="'.$ak.'"')->find();
	if($data == NULL){
		return 1;//û�и�ak
	}elseif($data == false){
		return 2;//��ѯ����
	}else{
		return 0;//�ɹ�
	}
}

function CheckUser($username){//�ж��Ƿ����ݱ��д����û���
	$mysql = M("rating_index");//�������ݿ�
	$data = $mysql->where('username="'.$username.'"')->find();//��ѯĳ���û���������Ϣ
	if($data == NULL){
		$new_data['username'] = $username;
		$mysql->data($new_data)->add();
	}
}

?>