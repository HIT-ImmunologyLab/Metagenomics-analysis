<?php
/**
 * Created by PhpStorm.
 * User: lyk
 * Date: 2017/6/10 0010
 * Time: 19:37
 */

namespace Home\Model;

use Think\Model;

class Bacteria2Model extends Model
{

    // 具有分页功能的细菌种类获取
    public function getAllCategory($limit, $number)
    {
        $arr = $this->field("count(*) as 'all'")->select();
        $bacteria = $this->order("id, parent_id asc")->limit($limit*$number . "," . $number)->select();
        $data['allLen'] = $arr;
        $data['data'] = $bacteria;
        return $data;
    }

    // 根据条件where获取细菌
    public function getSearchBacteria($where) {
        $data = $this->where($where)->select();
        return $data;
    }

    public function getFirstSpecieLevel($number) {
        $data = $this->where("level = 6")->limit("0, " . $number)->select();
        return $data;
    }

    public function getSpecieLevel($limit, $number) {
        $arr = $this->field("count(*) as 'all'")->select();
        $bacteria = $this->where("level = 6")->limit($limit*$number . ", " . $number)->select();
        $data['allLen'] = $arr;
        $data['data'] = $bacteria;
        return $data;
    }

    public function getFirstGenusLevel($number) {
        $data = $this->where("level = 5 AND is_last = false")->limit("0, " . $number)->select();
        return $data;
    }

    public function getGenusLevel($limit, $number) {
        $arr = $this->field("count(*) as 'all'")->select();
        $bacteria = $this->where("level = 5 AND is_last = false")->limit($limit*$number . ", " . $number)->select();
        $data['allLen'] = $arr;
        $data['data'] = $bacteria;
        return $data;
    }

    public function getSonBacteria($id) {
        $bacteria = $this->where("parent_id = " . $id . " AND is_last = true")->select();
        return $bacteria;
    }

    public function getSonBacteria2($id) {
        $bacteria = $this->where("parent_id = " . $id)->select();
        return $bacteria;
    }


//    public function getSonBacteria($type, $name) {
//        $arr = $this->where($type."='".$name."'")->select();
//        $bacteria = $this->where("parent_id = " . $arr[0]['parent_id'] . " AND is_last = true")->select();
//        return $bacteria;
//    }

    public function getBacteriaById($id) {
        $bacteria = $this->where("bacteria_id = '". $id . "'")->select();
        return $bacteria;
    }

    public function getThirdLevelBacteria() {
        $bacteria = $this->where("level < 3 ")->order("id asc")->select();
        return $bacteria;
    }

}