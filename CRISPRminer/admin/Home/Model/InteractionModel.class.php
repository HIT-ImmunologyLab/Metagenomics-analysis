<?php
/**
 * Created by PhpStorm.
 * User: lyk
 * Date: 2017/6/11 0011
 * Time: 22:08
 */

namespace Home\Model;

use Think\Model;

class InteractionModel extends Model
{

    public function getSpecieInteraction()
    {
        $interaction = $this->field("specie, count(distinct bacteria_id) as bacteria_num, count(distinct phage_id) as phage_num")->group("specie")->select();
        return $interaction;
    }

    public function getGenusInteraction()
    {
        $interaction = $this->field("genus, count(distinct bacteria_id) as bacteria_num, count(distinct phage_id) as phage_num")->group("genus")->select();
        return $interaction;
    }

    public function getDetails($kind, $value)
    {
        // $detail = $this->where($kind. " = '" . $value . "'")->select();
        //$detail = $this->table(array("Interaction", ))
        //return $detail;
    }

    // check某个细菌是否在interaction表中
    public function checkExists($bacteria_id, $spacerArr) {
        $arr = $this->where("bacteria_id = '". $bacteria_id ."'")->select();
        $result = array();
        if ( !count($arr) ) {
            $result['exist'] = 0;
            $result['data'] = null;
            return $result;
        }
        if ( count($spacerArr) ) {

            $flag = 0;
            $data = array();
            for ( $i=0; $i<count($spacerArr); $i++ ) {
                $arr3 = $this->where("bacteria_id = '". $bacteria_id . "' and spacer_id like '". $spacerArr[$i]['id'] ."%'")->select();
                for ( $k=0; $k<count($arr3); $k++ ) {
                    if ( array_key_exists("phage_id", $arr3[$k]) ) {
                        $flag = 1;
                        $arr2['spacer_id'] = $spacerArr[$i]['id'];
                        $arr2['data'] = $arr3;
                        array_push($data, $arr2);
                    }
                }
            }
            if ( $flag ) {
                $result['exist'] = 1;
                $result['data'] = $data;
                return $result;
            } else {
                $result['exist'] = 0;
                $result['data'] = null;
                return $result;
            }
        }
    }

}