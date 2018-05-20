<?php
/**
 * Created by PhpStorm.
 * User: lyk
 * Date: 2017/6/13 0013
 * Time: 14:57
 */
namespace Home\Controller;

use Think\Controller;

class BaseController extends Controller
{

    protected $ir; // interaction
    protected $b2; // bacteria2
    protected $st; // selftarget
    protected $sts; //subtypes
    protected $ac; // anticrispr
    protected $sg;

    protected function _initialize(){
        // 实例化各个数据表Model
        $this->ir = D("Interaction");
        $this->b2 = D("Bacteria2");
        $this->st = D("Selftarget");
        $this->sts = D("Subtypes");
        $this->ac = D("Anticrispr");
        $this->sg = D("Speciegenus");
    }
}