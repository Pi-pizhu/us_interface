from api.department_api import Department


class TestSeparate:

    def setup_class(self):
        self.department = Department()

    def test_add_tag(self):
        assert self.department.create(dep_name="王五", dep_name_en="wangwu", p_id=4)['errcode'] == 0

    def test_update_dep(self):
        dep_data = self.department.get_department(dep_id=4)
        dep_id = self.department.extract_variables(dep_data, expr='$..department[?(@.name=="王五")].id')[0]
        assert self.department.update(dep_id=dep_id, dep_name="张三", dep_name_en='zhangsan', p_id=2)['errcode'] == 0

    def test_get_department(self):
        assert self.department.get_department(dep_id=1)['errcode'] == 0

    def test_delete_tag(self):
        dep_data = self.department.get_department(dep_id=2)
        dep_id = self.department.extract_variables(dep_data, expr='$..department[?(@.name=="张三")].id')[0]
        assert self.department.delete(dep_id=dep_id)['errcode'] == 0