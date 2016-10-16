<?php
namespace Home\Controller;
use Think\Controller;
class ClearingController extends Controller {

    public function index(){
		
		$post_userA = I('post.usernameA','','strip_tags');//通过Post方法获取玩家A名称
		$post_userB = I('post.usernameB','','strip_tags');//通过Post方法获取玩家B名称
		$post_userA_socre = I('post.userscoreA','','strip_tags');//通过Post方法获取玩家A socre
		$post_userB_socre = I('post.userscoreB','','strip_tags');//通过Post方法获取玩家B socre
		
		$arena = I('post.arena','','strip_tags');//通过Post的方式获取玩家的比赛类型
		$safekey = I('post.accesskey','','strip_tags');//通过Post方法获取accesskey是否合法

		if(verifica($safekey) == 0){
			//判断用户胜负
				if($post_userA_socre > $post_userB_socre){
					$playerBname = $post_userA; //playerB 是胜利的
					$playerAname = $post_userB; //playerA 是败北的
				}elseif($post_userA_socre < $post_userB_socre){
					$playerBname = $post_userB; //playerB 是胜利的
					$playerAname = $post_userA; //playerA 是败北的
				}elseif($post_userA_socre == $post_userB_socre){
					$playerBname = $post_userB; //playerB 是胜利的
					$playerAname = $post_userA; //playerA 是败北的
					$draw = true;
				}else{
					error_return('500');
				}
			
			CheckUser($playerAname);
			CheckUser($playerBname);
			$playerAresult = 0;//第一个用户名为败北的
			$playerBresult = 1;//第二个用户名为胜利的
					
					
			$playerA = QueryData($playerAname); //获取玩家A的数据
			$playerB = QueryData($playerBname); //获取玩家B的数据
			
			
			if($arena == 'entertain'){//entertain:娱乐 ；athletic:竞技
				
				if($draw != true){//非平局
					$ratingA_B = ClearingExp($playerA['exp'],$playerB['exp'],$playerAname,$playerBname,$draw);
					
					UpdataExp($playerAname,$ratingA_B[0]['exp'],$playerA['game'] + 1,
									$playerA['win'],$playerA['lose'] + 1,$playerAresult);	
					UpdataExp($playerBname,$ratingA_B[1]['exp'],$playerB['game'] + 1,
									$playerB['win'] + 1,$playerB['lose'],$playerBresult);
					
				}else{//平局
					$ratingA_B = ClearingExp($playerA['exp'],$playerB['exp'],$playerAname,$playerBname,$draw);
					UpdataExp($playerAname,$ratingA_B[0]['exp'],$playerA['game'] + 1,
									$playerA['win'],$playerA['lose'],$playerAresult);
					UpdataExp($playerBname,$ratingA_B[1]['exp'],$playerB['game'] + 1,
									$playerB['win'],$playerB['lose'],$playerBresult);

				}								
			}elseif($arena == 'athletic'){
				if($draw != true){//非平局
					$ratingA_B = ClearingRating($playerA['pt'],$playerB['pt'],$playerAresult,$playerBresult,$playerAname,$playerBname); //清算ELO积分
					
					
					UpdataElo($playerAname,$ratingA_B[0]['pt'],$playerA['game'] + 1,
								$playerA['win'],$playerA['lose'] + 1,$playerAresult);
					UpdataElo($playerBname,$ratingA_B[1]['pt'],$playerB['game'] + 1,
								$playerB['win'] + 1,$playerB['lose'],$playerBresult);	
					
				}else{//平局
					$ratingA_B = ClearingRating($playerA['pt'],$playerB['pt'],'1','1',$playerAname,$playerBname); //清算ELO积分
					UpdataElo($playerAname,$ratingA_B[0]['pt'],$playerA['game'] + 1,
								$playerA['win'],$playerA['lose'],'1');
					UpdataElo($playerBname,$ratingA_B[1]['pt'],$playerB['game'] + 1,
								$playerB['win'],$playerB['lose'],'1');
				}
					
				
/* 				
				TrueSkill算法的
				$ratingA_B = Tureskill($playerA['u'],$playerB['u'],$playerA['o'],$playerB['o'],$playerAname,$playerBname);//计算出玩家ab的u和o	
				$ratingA_B = ClearingRating($playerA['u'],$playerB['u'],$playerA['o'],$playerB['o'],$playerAname,$playerBname);
				
				UpdataSkill($playerAname,$ratingA_B[0]['o'],$ratingA_B[0]['u'],$playerA['games'] + 1,
								$playerA['win'],$playerA['lose'] + 1,$playerAresult);
								
				UpdataSkill($playerBname,$ratingA_B[1]['o'],$ratingA_B[1]['u'],$playerB['games'] + 1,
								$playerB['win'] + 1,$playerB['lose'],$playerBresult); */
			}		
			
		}else{
			error_return('500');
		}
		}
}