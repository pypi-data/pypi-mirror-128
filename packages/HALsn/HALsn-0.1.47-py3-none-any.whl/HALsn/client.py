#! /usr/bin/python

from socketMaster import client
from dataSupervisor import dataSupervisor
from SKU import CFP
from sample_data.sample_data import data

sn_ip = '192.168.217.203'      # SHARKNINJA
hm_ip = '192.168.109.128'      # HOME VM

cfp = CFP(debug=True)

super = dataSupervisor(map=cfp.queries, headers=False, s3_enable=False)
super.parser.lst = data

super.generate()

cli = client(sn_ip, 5050)
cli.send_msg(cli.node, super.parser.df)
cli.send_msg(cli.node, '!DC')
