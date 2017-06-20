# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------
import os

def index():
    import pymongo
    from sklearn import metrics
    client = pymongo.MongoClient("localhost", 27017)
    db = client.datamining
    query = db.ranking.find()
    errormsg = ''


    pontos = []
    nomes = []

    for group in query:
        pontos.append(max(group['points_open']))
        nomes.append(group['dupla'])

    pontos, nomes = zip(*sorted(zip(pontos, nomes)))
    pontos = pontos[::-1]
    nomes = nomes[::-1]

    
    passwd = request.vars.password
    f = request.vars.fileToUpload

    errormsg = ''

    if passwd != None:
        try:
            query2 = db.ranking.find({"passwd": int(passwd)})[0]
            points_open = query2['points_open']
            max_open = max(query2['points_open'])
            points_hidden = query2['points_hidden']

        except IndexError:
            errormsg = "Grupo inexistente. Verifique a chave."

        except ValueError:
            errormsg = "Dupla precisa ser inteiro."

        try:
            ypred = [float(x) for x in f.file.readlines()]
            y = [float(x) for x in open(os.path.dirname(os.path.abspath(__file__))+'/../labels.csv').readlines()]
            open_auc = metrics.roc_auc_score(y[:len(y)/2], ypred[:len(y)/2])
            closed_auc = metrics.roc_auc_score(y[len(y)/2:], ypred[len(y)/2:])
            db.ranking.update({"passwd": int(passwd)},{'points_hidden': points_hidden.append(closed_auc)},{'points_open': points_open.append(closed_auc)})
            if max_open < open_auc:
                errormsg = "Seu score foi melhorado!"

        except Exception as e:
            errormsg = "formato inválido"
            pass

    return dict(nomes=nomes, pontos=pontos, errormsg=errormsg)


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


