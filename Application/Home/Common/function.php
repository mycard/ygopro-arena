<?php

function ClearingRating($ratingA,$ratingB,$resultA,$resultB,$usernameA,$usernameB){//������ʷ����
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

function ClearingTempRating($ratingA,$ratingB,$resultA,$resultB,$usernameA,$usernameB){//�����������
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

function UpdataRating($username,$rating,$temprating,$games,$tempgames,$win,$tempwin,$lose,$templose,$last){//�����û�
	$mysql = M("rating_index");
	$data['integral'] = $rating; //�ܻ���
	$data['tempinte'] = $temprating; //�������
	$data['games'] = $games; //�ܳ���
	$data['tempgames'] = $tempgames; //���峡��
	$data['win'] = $win; //��ʤ��
	$data['tempwin'] = $tempwin; //����ʤ��
	$data['lose'] = $lose; //��ʧ��
	$data['templose'] = $templose; //����ʧ��
	$data['last'] = $last; //���һ����Ӯ
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

function Ranking(){//��ȡȫ����һ��ֵ�ǰʮ��
	$mysql = M("rating_index");//�������ݱ�
	$data = $mysql->where('status=0')->field('username')->order('tempinte desc')->limit(10)->select();//��ȡ����ǰʮ��
	return $data;//��������
}

function Ranking_player($tempinte){//�����û�Ŀǰ��������������õ�
	$mysql = M("rating_index");//�������ݿ�
	$map['tempinte'] = array('EGT',$tempinte);//�����鵱����ѯ����
	$data = $mysql->where($map)->field('username')->order('tempinte asc,username asc')->Count();//������û��������������
	return $data;//��������
}

function UpdataStatus($username,$status){//�����û��Ƿ����ߵ�
	$mysql = M("rating_index");
	$data['online'] = $status;
	$mysql->where('username="'.$username.'"')->save($data); //��������
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