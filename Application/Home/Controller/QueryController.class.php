<?php
namespace Home\Controller;
use Think\Controller;
class QueryController extends Controller {
    public function index(){
		$player = I('get.username','','strip_tags');//通过Post方法获取玩家名称
		//$passw = I('post.password','','strip_tags');//通过Post方法获取玩家密码
		//$safekey = I('post.ak','','strip_tags');//通过Post方法获取是否合法
		
			CheckUser($player);
			$player_data = QueryData($player); //获取玩家的数据
			if($player_data == NULL){
				error_return('404');
			}
				$EndResult = array(
						'exp'=>$player_data['exp'],
						'pt'=>$player_data['pt'],
						'trueskill'=>array(
							'mean'=>$player_data['u'],
							'variance'=>$player_data['o']
						)
					);
			$this->ajaxReturn($EndResult);
		

		
		}
}