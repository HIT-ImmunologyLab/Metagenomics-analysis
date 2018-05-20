<?php
namespace Home\Controller;
use Think\Controller;
class QueryinfoController extends Controller{
	public function index(){
	}
	public function queryPage(){
		$m = M("microbiome2disease");
		$count = $m->where()->count();
		$page = new \Org\Pageclass\Page($count,10);
		$show = $page->show();
		$info = $m->where()->limit($page->firstRow.','.$page->listRows)->select();
		$this->assign('info',$info);
		$this->assign('page',$show);
		$this->display();
	}
	//用于批量导入测试数据，每次添加10条
	/*
	public function crowadd(){
		$m = M("microbiome2disease");
		$data = array();
		$data[] = array('domain'=>'dontknow', 'phylum'=>'dontknow', 'class'=>'dontknow', 'subclass'=>'dontknow', 'order'=>'dontknow', 'suborder'=>'dontknow', 'family'=>'dontknow', 'genus'=>'dontknow', 'spacies'=>'dontknow', 'note'=>'dontknow', 'searchResult'=>'NA', 'phenotype'=>'dontknow', 'diseaseHost'=>'human', 'pathway'=>'dontknow', 'protein'=>'dontknow', 'compound'=>'dontknow', 'paperTitle'=>'dontknow', 'pubmedID'=>1, 'doi'=>'dontknow', 'method'=>'dontknow', 'otherNotes'=>'dontknow');
		$data[] = array('domain'=>'dontknow', 'phylum'=>'dontknow', 'class'=>'dontknow', 'subclass'=>'dontknow', 'order'=>'dontknow', 'suborder'=>'dontknow', 'family'=>'dontknow', 'genus'=>'dontknow', 'spacies'=>'dontknow', 'note'=>'dontknow', 'searchResult'=>'NA', 'phenotype'=>'dontknow', 'diseaseHost'=>'human', 'pathway'=>'dontknow', 'protein'=>'dontknow', 'compound'=>'dontknow', 'paperTitle'=>'dontknow', 'pubmedID'=>1, 'doi'=>'dontknow', 'method'=>'dontknow', 'otherNotes'=>'dontknow');
		$data[] = array('domain'=>'dontknow', 'phylum'=>'dontknow', 'class'=>'dontknow', 'subclass'=>'dontknow', 'order'=>'dontknow', 'suborder'=>'dontknow', 'family'=>'dontknow', 'genus'=>'dontknow', 'spacies'=>'dontknow', 'note'=>'dontknow', 'searchResult'=>'NA', 'phenotype'=>'dontknow', 'diseaseHost'=>'human', 'pathway'=>'dontknow', 'protein'=>'dontknow', 'compound'=>'dontknow', 'paperTitle'=>'dontknow', 'pubmedID'=>1, 'doi'=>'dontknow', 'method'=>'dontknow', 'otherNotes'=>'dontknow');
		$data[] = array('domain'=>'dontknow', 'phylum'=>'dontknow', 'class'=>'dontknow', 'subclass'=>'dontknow', 'order'=>'dontknow', 'suborder'=>'dontknow', 'family'=>'dontknow', 'genus'=>'dontknow', 'spacies'=>'dontknow', 'note'=>'dontknow', 'searchResult'=>'NA', 'phenotype'=>'dontknow', 'diseaseHost'=>'human', 'pathway'=>'dontknow', 'protein'=>'dontknow', 'compound'=>'dontknow', 'paperTitle'=>'dontknow', 'pubmedID'=>1, 'doi'=>'dontknow', 'method'=>'dontknow', 'otherNotes'=>'dontknow');
		$data[] = array('domain'=>'dontknow', 'phylum'=>'dontknow', 'class'=>'dontknow', 'subclass'=>'dontknow', 'order'=>'dontknow', 'suborder'=>'dontknow', 'family'=>'dontknow', 'genus'=>'dontknow', 'spacies'=>'dontknow', 'note'=>'dontknow', 'searchResult'=>'NA', 'phenotype'=>'dontknow', 'diseaseHost'=>'human', 'pathway'=>'dontknow', 'protein'=>'dontknow', 'compound'=>'dontknow', 'paperTitle'=>'dontknow', 'pubmedID'=>1, 'doi'=>'dontknow', 'method'=>'dontknow', 'otherNotes'=>'dontknow');
		$data[] = array('domain'=>'dontknow', 'phylum'=>'dontknow', 'class'=>'dontknow', 'subclass'=>'dontknow', 'order'=>'dontknow', 'suborder'=>'dontknow', 'family'=>'dontknow', 'genus'=>'dontknow', 'spacies'=>'dontknow', 'note'=>'dontknow', 'searchResult'=>'NA', 'phenotype'=>'dontknow', 'diseaseHost'=>'human', 'pathway'=>'dontknow', 'protein'=>'dontknow', 'compound'=>'dontknow', 'paperTitle'=>'dontknow', 'pubmedID'=>1, 'doi'=>'dontknow', 'method'=>'dontknow', 'otherNotes'=>'dontknow');
		$data[] = array('domain'=>'dontknow', 'phylum'=>'dontknow', 'class'=>'dontknow', 'subclass'=>'dontknow', 'order'=>'dontknow', 'suborder'=>'dontknow', 'family'=>'dontknow', 'genus'=>'dontknow', 'spacies'=>'dontknow', 'note'=>'dontknow', 'searchResult'=>'NA', 'phenotype'=>'dontknow', 'diseaseHost'=>'human', 'pathway'=>'dontknow', 'protein'=>'dontknow', 'compound'=>'dontknow', 'paperTitle'=>'dontknow', 'pubmedID'=>1, 'doi'=>'dontknow', 'method'=>'dontknow', 'otherNotes'=>'dontknow');
		$data[] = array('domain'=>'dontknow', 'phylum'=>'dontknow', 'class'=>'dontknow', 'subclass'=>'dontknow', 'order'=>'dontknow', 'suborder'=>'dontknow', 'family'=>'dontknow', 'genus'=>'dontknow', 'spacies'=>'dontknow', 'note'=>'dontknow', 'searchResult'=>'NA', 'phenotype'=>'dontknow', 'diseaseHost'=>'human', 'pathway'=>'dontknow', 'protein'=>'dontknow', 'compound'=>'dontknow', 'paperTitle'=>'dontknow', 'pubmedID'=>1, 'doi'=>'dontknow', 'method'=>'dontknow', 'otherNotes'=>'dontknow');
		$data[] = array('domain'=>'dontknow', 'phylum'=>'dontknow', 'class'=>'dontknow', 'subclass'=>'dontknow', 'order'=>'dontknow', 'suborder'=>'dontknow', 'family'=>'dontknow', 'genus'=>'dontknow', 'spacies'=>'dontknow', 'note'=>'dontknow', 'searchResult'=>'NA', 'phenotype'=>'dontknow', 'diseaseHost'=>'human', 'pathway'=>'dontknow', 'protein'=>'dontknow', 'compound'=>'dontknow', 'paperTitle'=>'dontknow', 'pubmedID'=>1, 'doi'=>'dontknow', 'method'=>'dontknow', 'otherNotes'=>'dontknow');
		$data[] = array('domain'=>'dontknow', 'phylum'=>'dontknow', 'class'=>'dontknow', 'subclass'=>'dontknow', 'order'=>'dontknow', 'suborder'=>'dontknow', 'family'=>'dontknow', 'genus'=>'dontknow', 'spacies'=>'dontknow', 'note'=>'dontknow', 'searchResult'=>'NA', 'phenotype'=>'dontknow', 'diseaseHost'=>'human', 'pathway'=>'dontknow', 'protein'=>'dontknow', 'compound'=>'dontknow', 'paperTitle'=>'dontknow', 'pubmedID'=>1, 'doi'=>'dontknow', 'method'=>'dontknow', 'otherNotes'=>'dontknow');
		$m->addAll($data);
		echo "导入完毕";
		}
	*/
}