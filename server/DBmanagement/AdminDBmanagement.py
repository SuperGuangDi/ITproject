# -*- coding=utf-8 -*-

from server.data.DBContext import DBContext
from server.mutex.State import State
from server.mutex import Tools

_sql_unreviewed_book = "select bookid, name, price, detail, isbn, number, picture, state, author, class, time from book natural join user_book_publish where state = \"待审核\";"
_sql_reviewed_book = "select bookid, name, price, detail, isbn, number, picture, state, author, class, time from book natural join user_book_publish where state is not '待审核' or state is not '未通过';"
_sql_user_info = "select userid, address, phone, idnumber, name from user;"
_sql_book_admin = "insert into book_admin(bookid, adminid) values (?,?);"
_sql_check_order = "select buyerid, sellerid, orders.total, book.name, orders.state from user_order join orders using (bookid, orderid) join book using (bookid)"
_key_book_info = ('bookid', 'name', 'price', 'detail', 'ISBN', 'number', 'picture', 'state', 'author', 'class', 'time')
_key_user_info = ('userid', 'address', 'phone', 'idnumber', 'name')
_key_order_info = ('buyerid', 'sellerid', 'price', 'bookname', 'orderstate')


class AdminDBmanagement(object):
    @staticmethod
    def admin_login(adminid, pwd):
        #管理员登录
        _sql_admin_login = "select * from admin where adminid=? and password=?;"
        with DBContext() as con:
            if not con.exec(_sql_admin_login, (adminid, pwd)):
                return {'state': State.Error}
            res = con.get_cursor().fetchone()
            if not res:
                return {'state': State.Error}
            return {'state': State.OK}
        pass


    @staticmethod
    def admin_register():
        '''
        默认注册6个管理员
        往后暂不提供注册功能
        '''
        _sql_admin_reg = "insert into admin values (?,?);"
        _const_admin = [
            ('gydi', 'gydi'), ('jiashuo', 'jiashuo'), ('chang', 'chang'),
            ('wujie', 'wujie'), ('guangyun', 'guangyun'), ('shijie', 'shijie'),
            ('test', 'test'), ('other', 'other')
        ]
        with DBContext() as con:
            con.get_cursor().executemany(_sql_admin_reg, _const_admin)
            if con.is_error():
                return {'state': State.DBErr}
            return {'state': State.OK}
        pass

    @staticmethod
    def view_publish():
        pass

    @staticmethod
    def search_unreviewed_book():
        # 查询未审核的书
        with DBContext() as con:
            if not con.exec(_sql_unreviewed_book):
                return {'state': State.DBErr}
            tempList = con.get_cursor().fetchall()
        try:
            res = Tools.list_tuple2dict(_key_book_info, tempList)
        except:
            return {'state': State.Error}
        return {'state': State.OK, 'booklist': res}
    pass

    @staticmethod
    def search_reviewed_book():
        # 查询已审核的书
        with DBContext() as con:
            if not con.exec(_sql_reviewed_book):
                return {'state': State.DBErr}
            tempList = con.get_cursor().fetchall()
        try:
            res = Tools.list_tuple2dict(_key_book_info, tempList)
        except:
            return {'state': State.Error}
        return {'state': State.OK, 'booklist': res}
    pass

    @staticmethod
    def view_user():
        # 查看用户信息
        with DBContext() as con:
            if not con.exec(_sql_user_info):
                return {'state': State.DBErr}
            userList = con.get_cursor().fetchall()
        try:
            res = Tools.list_tuple2dict(_key_user_info, userList)
        except:
            return {'state': State.Error}
        return {'state': State.OK, 'userlist': res}
    pass

    @staticmethod
    def add_book_admin_table(bookid, adminid):
        #添加管理员与审核书籍的关系
        with DBContext() as con:
            if not con.exec(_sql_book_admin, (bookid, adminid)):
                return {'state': State.DBErr}
            return {'state': State.OK}
        pass

    @staticmethod
    def check_order():
        #查看订单
        with DBContext() as con:
            if not con.exec(_sql_check_order):
                return {'state': State.DBErr}
            orderlist = con.get_cursor().fetchall()
            try:
                res = Tools.list_tuple2dict(_key_order_info, orderlist)
            except:
                return {'state': State.Error}
            return {'state': State.OK, 'orderlist': res}
        pass


