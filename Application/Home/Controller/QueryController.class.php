<?php
namespace Home\Controller;

use Think\Controller;

class QueryController extends Controller
{
    public function index()
    {
        $player = I('get.username', '', 'strip_tags');//通过Post方法获取玩家名称
        
        //profile前端页面需要的全部数据  全部初始化为0    add by Joe 20160921
        $EndResult = array(
            'exp' => '0',
            'exp_rank' => '0',
            'pt' => '0',
            'arena_rank' => '0',
            'win' => '0',
            'lose' => '0',
            'draw' => '0',
            'all' => '0',
            'ratio' => '0',
            'violation' => '0',
        );
        
        //TODO CheckUser 和 QueryData  永远返回false , bug ?
        CheckUser($player);
        $player_data = QueryData($player); //获取玩家的数据
        
        //TODO 开发约定: QueryData($player); 业务层返回给Controller层 不要返回null ,可以与上面$EndResult 一样设置默认值,
        // 排名 和 胜率 之类数据库不能直接查到 或需要计算的字段, 在方法内部处理
        if($player_data != NULL){
            $EndResult['exp'] = $player_data['exp'] ;
            $EndResult['exp_rank'] = $player_data['exp'] ;
            $EndResult['pt'] = $player_data['exp'] ;
            $EndResult['arena_rank'] = $player_data['exp'] ;
            $EndResult['win'] = $player_data['exp'] ;
            $EndResult['lose'] = $player_data['exp'] ;
            $EndResult['draw'] = $player_data['exp'] ;
            $EndResult['all'] = $player_data['exp'] ;
            $EndResult['ratio'] = $player_data['exp'] ;
            $EndResult['violation'] = $player_data['exp'] ;
        }
        
        // 设置允许跨域访问 , 可以把*改成域名
        header('Access-Control-Allow-Origin: *');
        $this->ajaxReturn($EndResult);
    }
}
