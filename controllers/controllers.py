# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################
import io
from reportlab.pdfgen import canvas
import base64
from operator import itemgetter

from odoo import http, _
from odoo.addons.portal.controllers.portal import CustomerPortal, pager
from odoo.addons.web.controllers.main import serialize_exception, content_disposition
from odoo.http import request
from odoo.osv.expression import OR
from odoo.tools import groupby as groupbyelem


class HospitalPortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        vals = super(HospitalPortal, self)._prepare_home_portal_values(counters)
        # new code
        user_id = request.env.uid
        offices_list = request.env['hospital.clinic.tickets'].search([
            ('portal_user_id', '=', user_id)
        ]).ids

        offices_domain = []
        if offices_list:
            offices_domain = OR(
                [offices_domain, [('offices_id', '=', offices_list)]])

        vals['maids_count'] = request.env['hospital.clinic.tickets'].search_count(
            offices_domain)

        return vals

    @http.route(route=['/my/tickets', '/my/tickets/page/<int:page>'], type="http", website=True, auth='user')
    def my_maids_list_view(self, page=1, sortby='ida', groupby="none", search="", search_in="all", **kw):
        vals = super()._prepare_portal_layout_values()
        # prepare
        user_id = request.env.uid

        offices_list = request.env['housemaid.offices'].search([
            ('portal_user_id', '=', user_id)
        ]).ids

        maids_domain = []
        if offices_list:
            maids_domain = OR(
                [maids_domain, [('offices_id', '=', offices_list)]])

        vals['maids_count'] = request.env['housemaid.maids'].search_count(
            maids_domain)
        #

        searchbar_sortings = self._get_searchbar_sortings()
        # default sort by order
        if not sortby:
            sortby = 'ida'
        searchbar_inputs = self._get_searchbar_inputs

        order = searchbar_sortings[sortby]['order']

        searchbar_groupby = self._get_searchbar_groupby()
        if not groupby:
            groupby = 'none'

        maids_group_by = searchbar_groupby.get(groupby, {})
        if groupby in ('jobs_id', 'state', 'country_id'):
            maids_group_by = maids_group_by.get('input')
            order = maids_group_by + ',' + order
        else:
            maids_group_by = ''

        search_domain = []
        # add value domain to dict
        if search and search_in:
            search_domain += self._get_search_domain(search_in, search)

        # return domain key and value
        # search_domain = searchbar_inputs[search_in]['search_domain']

        # append search domain to maid domain
        if search_domain:
            maids_domain += search_domain

        total_maids = request.env['housemaid.maids'].sudo(
        ).search_count(maids_domain)

        maid_url = '/my/maids/'
        pager_detail = pager(
            url=maid_url,
            url_args={'sortby': sortby,
                      'groupby': groupby,
                      'search_in': search_in,
                      'search': search},
            total=total_maids,
            page=page,
            step=10,
        )
        maids_obj = request.env['housemaid.maids']
        maids = request.env['housemaid.maids'].sudo().search(
            maids_domain,
            limit=10,
            order=order,
            offset=pager_detail['offset'],
        )
        maids_group_list = []
        # # start groupby after maids search
        if maids_group_by:
            maids_group_list = [{
                maids_group_by: k,
                'maids': maids_obj.concat(*g)
            } for k, g in groupbyelem(maids, itemgetter(maids_group_by))]
        else:
            maids_group_list = [{maids_group_by: '', 'maids': maids}]

        vals.update({
            'default_url': maid_url,
            'maids': maids,
            'group_maids': maids_group_list,
            'page_name': 'my_maids_portal_list_view',
            'pager': pager_detail,
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
            'searchbar_groupby': searchbar_groupby,
            'groupby': groupby,
            'search_in': search_in,
            'searchbar_inputs': searchbar_inputs,
            'search': search,
        })

        return request.render(
            "ms_housemaid.my_maids_portal_list_view",
            vals,
        )

    @http.route(route=['/my/patients', '/my/patients/page/<int:page>'], type="http", website=True, auth='user')
    def my_maids_list_view(self, page=1, sortby='ida', groupby="none", search="", search_in="all", **kw):
        vals = super()._prepare_portal_layout_values()
        # prepare
        user_id = request.env.uid

        offices_list = request.env['housemaid.offices'].search([
            ('portal_user_id', '=', user_id)
        ]).ids

        maids_domain = []
        if offices_list:
            maids_domain = OR(
                [maids_domain, [('offices_id', '=', offices_list)]])

        vals['maids_count'] = request.env['housemaid.maids'].search_count(
            maids_domain)
        #

        searchbar_sortings = self._get_searchbar_sortings()
        # default sort by order
        if not sortby:
            sortby = 'ida'
        searchbar_inputs = self._get_searchbar_inputs

        order = searchbar_sortings[sortby]['order']

        searchbar_groupby = self._get_searchbar_groupby()
        if not groupby:
            groupby = 'none'

        maids_group_by = searchbar_groupby.get(groupby, {})
        if groupby in ('jobs_id', 'state', 'country_id'):
            maids_group_by = maids_group_by.get('input')
            order = maids_group_by + ',' + order
        else:
            maids_group_by = ''

        search_domain = []
        # add value domain to dict
        if search and search_in:
            search_domain += self._get_search_domain(search_in, search)

        # return domain key and value
        # search_domain = searchbar_inputs[search_in]['search_domain']

        # append search domain to maid domain
        if search_domain:
            maids_domain += search_domain

        total_maids = request.env['housemaid.maids'].sudo(
        ).search_count(maids_domain)

        maid_url = '/my/maids/'
        pager_detail = pager(
            url=maid_url,
            url_args={'sortby': sortby,
                      'groupby': groupby,
                      'search_in': search_in,
                      'search': search},
            total=total_maids,
            page=page,
            step=10,
        )
        maids_obj = request.env['housemaid.maids']
        maids = request.env['housemaid.maids'].sudo().search(
            maids_domain,
            limit=10,
            order=order,
            offset=pager_detail['offset'],
        )
        maids_group_list = []
        # # start groupby after maids search
        if maids_group_by:
            maids_group_list = [{
                maids_group_by: k,
                'maids': maids_obj.concat(*g)
            } for k, g in groupbyelem(maids, itemgetter(maids_group_by))]
        else:
            maids_group_list = [{maids_group_by: '', 'maids': maids}]

        vals.update({
            'default_url': maid_url,
            'maids': maids,
            'group_maids': maids_group_list,
            'page_name': 'my_maids_portal_list_view',
            'pager': pager_detail,
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
            'searchbar_groupby': searchbar_groupby,
            'groupby': groupby,
            'search_in': search_in,
            'searchbar_inputs': searchbar_inputs,
            'search': search,
        })

        return request.render(
            "ms_housemaid.my_maids_portal_list_view",
            vals,
        )

    @http.route('/ms_hospital/download_pdf_hello_world', type='http', auth="public")
    def download_pdf_hello_world(self, **kwargs):
        response = http.Response()
        pdf_file = io.BytesIO()
        pdf = canvas.Canvas(pdf_file)
        pdf.drawString(100, 750, "Hello World")
        pdf.save()
        pdf_file.seek(0)
        response.stream.write(pdf_file.read())
        response.stream.flush()
        response.headers.set('Content-Disposition', 'attachment; filename="hello_world.pdf"')
        response.set_cookie('fileToken', 'hello_world')
        response.status = '200 OK'
        response.content_type = 'application/pdf'
        return response
