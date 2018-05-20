<?php
/**
 * Created by PhpStorm.
 * User: lyk
 * Date: 2017/6/29 0029
 * Time: 22:28
 */

namespace Home\Model;

use Think\Model;

class SpeciegenusModel extends Model
{
    public function getPieDataForGenus() {
        $arr = $this->field("distinct genus as name, count(lineage) as value")->group("genus")->order("value desc")->select();
        return $arr;
    }

    public function getPieDataForSpecie() {
        $arr = $this->field("distinct specie as name, count(lineage) as value")->group("specie")->order("value desc")->select();
        return $arr;
    }

    public function getSpecieLevel($limit, $number) {
        $arr = $this->field("count(distinct specie) as 'all'")->select();
//        $bacteria = $this->where("level = 6")->limit($limit*$number . ", " . $number)->select();
        $specie = $this->field("distinct specie, count(lineage) as num")->limit($limit*$number . ", " . $number)->group("specie")->select();
        $data['allLen'] = $arr;
        $data['data'] = $specie;
        return $data;
    }

    public function getGenusLevel($limit, $number) {
        $arr = $this->field("count(distinct genus) as 'all'")->select();
//        $bacteria = $this->where("level = 5 AND is_last = false")->limit($limit*$number . ", " . $number)->select();
        $genus = $this->field("distinct genus, count(lineage) as num")->limit($limit*$number . ", " . $number)->group("genus")->select();
        $data['allLen'] = $arr;
        $data['data'] = $genus;
        return $data;
    }

    public function getAllLineageForType($type, $name) {
        $arr = $this->where($type."='".$name."'")->select();
        return $arr;
    }

}