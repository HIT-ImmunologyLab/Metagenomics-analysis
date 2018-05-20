<?php
namespace Home\Controller;
use Think\Controller;
class AddinfoController extends Controller{
	public function index(){	
	}
	public function addPage(){
	    $this->queryInfo();
		$this->display();
	}
	public function addinfo(){
		$data['domain'] = $_POST['domain'];
		$data['phylum'] = $_POST['phylum'];
		$data['class'] = $_POST['class'];
		$data['subclass'] = $_POST['subclass'];
		$data['order'] = $_POST['order'];
		$data['suborder'] = $_POST['suborder'];
		$data['family'] = $_POST['family'];
		$data['genus'] = $_POST['genus'];
		$data['species'] = $_POST['species'];
		$data['note'] = $_POST['note'];
		$data['abstract'] = $_POST['abstract'];
		$data['microbiota'] = $_POST['microbiota'];
		$data['choosetype'] = $_POST['choosetype'];
		$data['searchResult'] = $_POST['searchResult'];
		$data['phenotype'] = $_POST['phenotype'];
		$data['diseaseHost'] = $_POST['diseaseHost'];
		$data['pathway'] = $_POST['pathway'];
		$data['protein'] = $_POST['protein'];
		$data['compound'] = $_POST['compound'];
		$data['paperTitle'] = $_POST['paperTitle'];
		$data['pubmedID'] = $_POST['pubmedID'];
		$data['doi'] = $_POST['doi'];
		$data['method'] = $_POST['method'];
		$data['otherNotes'] = $_POST['otherNotes'];
        $counter = $_POST['counter'];
		$m = M();
		$m->startTrans();
		//$m2 = M("microbiome2disease_microbiota");
		$msg = $m->table('microbiome2disease')->create($data);
		//检查是否有doi或pubmedID重复
        if (!empty($data['doi'])) {
            $doi = $data['doi'];
            $doiRepeat = $m->table('microbiome2disease')->where("doi = $doi")->select();
        }else{
            $doiRepeat = NULL;
        }
        if(!empty($data['pubmedID'])) {
            $pubmedID = $data['pubmedID'];
            $pubmedIDRepeat = $m->table('microbiome2disease')->where("pubmedID = $pubmedID")->select();
        }else{
            $pubmedIDRepeat = NUll;
        }
        if (empty($doiRepeat)&&empty($pubmedIDRepeat)) {
            $result = $m->table('microbiome2disease')->add($data);
            //取主表id
            $mid = $m->table('microbiome2disease')->getLastInsID();
            //向关联表添加外键
            for($i = $counter; $i>=1; $i--){
                $data2['mid'] = $mid;
                $data2['microbiota'] = $_POST['microbiota'.$i];
                $data2['type'] = $_POST['choosetype'.$i];
                $msg2 = $m->table('microbiome2disease_microbiota')->create($data2);
                $result2 = $m->table('microbiome2disease_microbiota')->add($data2);
            }
            if($result == true){
                $m->commit();
                $this->success("添加成功");
            }else{
                $m->rollback();
                $this->error("添加失败");
            }
        }else{
            $this->error("doi或pubmedID已存在");
        }
	}
	public function queryInfo(){
	    $m = M();
	    $count = $m->table('microbiome2disease')->where()->count();
        $page = new \Org\Pageclass\Page($count,10);
        $show = $page->show();
        $info = $m->table('microbiome2disease')->where()->limit($page->firstRow.','.$page->listRows)->select();//        $info = $m->table('microbiome2disease')->where()->select();
        foreach($info as &$value){
            $id = $value['id'];
            $map['mid'] = array('eq', $id);
            $mics = $m->table('microbiome2disease_microbiota')->where($map)->select();
            $mcount = count($mics ,0);
            $value['mics'] = $mics;
            $value['mcount'] = $mcount;
            $mics = array();
            $mcount = 0;
        }
//        foreach ($info as $value){
//            echo "crow";
//            echo '<br/>';
//        }
        $this->assign('info',$info);
        $this->assign('page',$show);
    }
}