# -*- coding=utf-8 -*-

from server.data.DBContext import DBContext
from server.mutex.State import State
from server.mutex import Tools
import time
import random

_sql_search = "select bookid, name, price, detail, ISBN, number, picture, state, author, class from book where name like ? and state != '待审核';"
_sql_getbook_info = "select bookid, name, price, detail, ISBN, number, picture, state, author, class from book where bookid=?;"
_sql_insert_collect = "insert into User_Book_Collect values(?, ?, ?);"
_sql_get_sellerid = "select sellerid from user_book_publish where userid=?;"
_sql_modify_state = "update book set state = ? where bookid = ?;"
_sql_get_class = "select bookid, name, price, detail, ISBN, number, picture, state, author, class from book where class=? and state != '待审核';"
_sql_recommand = "select bookid, name, price, detail, ISBN, number, picture, state, author, class from book where state == '待售';"
_key_book_info = ('bookid', 'name', 'price', 'detail', 'ISBN',
                  'number', 'picture', 'state', 'author', 'class')
_book_class = ('计算机', '工程科学', '经济管理', '自然科学', '英语', '数学', '文学艺术', '政治法律', '其他')
_sql_delete_book = "update book set state=? where bookid=?;"
_key_book_info = ('bookid', 'name', 'price', 'detail', 'ISBN', 'number', 'picture', 'state', 'author', 'class')


class BookDBmanagement(object):

    @staticmethod
    def getSearchBook(keyword):
        # 通过关键字查询书籍列表
        # 构造模糊搜索
        fuzzy = "%" + keyword + "%"
        with DBContext() as con:
            if not con.exec(_sql_search, (fuzzy,)):
                return {'state': State.DBErr}
            tempList = con.get_cursor().fetchall()
        try:
            res = Tools.list_tuple2dict(_key_book_info, tempList)
        except:
            return {'state': State.Error}
        return {'state': State.OK, 'booklist': res}
    pass

    @staticmethod
    def getSellerID(bookid):
        with DBContext() as con:
            if not con.exec(_sql_get_sellerid, (bookid,)):
                return {'state': State.DBErr}
            res = con.get_cursor().fetchone()
            return {'state': State.OK, 'userid': res}
        pass
    pass

    @staticmethod
    def getBookInfo(bookid):
        # 通过书籍id查询书籍信息
        with DBContext() as con:
            if not con.exec(_sql_getbook_info, (bookid,)):
                return {'state': State.DBErr}
            tempList = con.get_cursor().fetchone()
            if not tempList:
                return {'state': State.BookNExit}
            return {'state': State.OK, 'bookinfo': Tools.tuple2dict(_key_book_info, tempList)}
        pass
    pass

    @staticmethod
    def changeBookState(bookid, newstate):
        # 更改书籍状态
        with DBContext() as con:
            if not con.exec("select state from book where bookid=?;", (bookid,)):
                return {'state': State.DBErr}
            res = con.get_cursor().fetchone()
            if not res:
                return {'state': State.Error}
            if res[0] != "待审核" and newstate != '待售' and newstate != '审核失败':
                return {'state': State.Debug}
            if not con.exec(_sql_modify_state, (newstate, bookid)):
                return {'state': State.DBErr}
            return {'state': State.OK}
        pass
    pass

    @staticmethod
    def get_class_books(bookclass):
        # 根据书籍的分类来获取书籍的列表
        if bookclass not in _book_class:
            return {'state': State.FormErr}
        with DBContext() as con:
            if not con.exec(_sql_get_class, (bookclass,)):
                return {'state': State.DBErr}
            res = con.get_cursor().fetchall()
            if not res:
                return {'state': State.ListNone}
            try:
                res = Tools.list_tuple2dict(_key_book_info, res)
            except:
                return {'state': State.Error}
            return {'state': State.OK, 'booklist': res}
        pass


    @staticmethod
    def get_recommand(max_fetch):
        # 根据传入的最大获取数来获取数据
        # 获取 推荐的 书籍
        if not isinstance(max_fetch, int):
            return {'state': State.Error}
        with DBContext() as con:
            if not con.exec(_sql_recommand):
                return {'state': State.DBErr}
            res = con.get_cursor().fetchmany(max_fetch)
            if not res:
                return {'state': State.ListNone}
            try:
                res = Tools.list_tuple2dict(_key_book_info, res)
            except:
                return {'state': State.Error}
            return {'state': State.OK, 'booklist': res}
        pass

    @staticmethod
    def sold_out_book(bookid):
        #下架书籍
        with DBContext() as con:
            if not con.exec("select state from book where bookid=?;", (bookid,)):
                return {'state': State.DBErr}
            res = con.get_cursor().fetchone()
            if not res:
                return {'state': State.DBErr}
            if res[0] == '下架':
                return {'state': State.Debug}
            if not con.exec(_sql_delete_book, ('下架', bookid)):
                return {'state': State.DBErr}
            return {'state': State.OK}
        pass


