<?php 

namespace Home\Controller;

class LocationController extends BaseController
{

	private $num;
	private $allData;

	public function __construct() {
		parent::__construct();
		$ar = D('access_records');
		$this->num = $ar->where("ip not like '%unknown%'")->count();
		$this->allData = $ar->where("ip not like '%unknown%'")->order("last_access desc")->select();
	}

	public function location()
	{
		$curPage = 1;
		if ( isset($_GET) && isset($_GET['page']) ) {
			$curPage = intval($_GET['page']);
		}
		$data = array_slice($this->allData, ($curPage-1)*10, 10);
		foreach($data as $key=>$da ) {
			$data[$key]['last_access'] = date('Y-m-d H:i:s', intval($da['last_access']));
		}
		$this->assign('count', $this->num);
		$this->assign('data', $data);
		$this->assign('pages', ceil($this->num/10));
		$this->assign('current', $curPage);
		$this->display();
	}
}