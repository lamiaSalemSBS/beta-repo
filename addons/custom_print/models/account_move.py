# -*- coding: utf-8 -*-
from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'


    ac_buyer_order_no = fields.Char(string="Buyer's Order No",
                                    related='invoice_line_ids.sale_line_ids.order_id.buyer_order_no',
                                    store=True,
                                    readonly=False
                                    )

    ac_proforma_invoice_date = fields.Date(string="Proforma Invoice Date",
                                           related = 'invoice_line_ids.sale_line_ids.order_id.proforma_invoice_date',
                                           store = True,
                                           readonly = False
                                           )


    ac_buyer_order_date = fields.Date(
        string="Buyer's Order Date",
        related='invoice_line_ids.sale_line_ids.order_id.buyer_order_date',
        store=True,
        readonly=False
    )
    ac_payment_term = fields.Many2one('account.payment.term',string="Payment Term",
                                      related='invoice_line_ids.sale_line_ids.order_id.payment_term_id',
                                      store=True,
                                      readonly=False
                                      )

    ac_incoterm = fields.Many2one('account.incoterms',string="Incoterm",
                                  related='invoice_line_ids.sale_line_ids.order_id.incoterm',
                                  store=True,
                                  readonly=False
                                  )
    ac_place_of_loading = fields.Char(string='Place of Loading',
                                      related='invoice_line_ids.sale_line_ids.order_id.place_of_loading',
                                      store=True,
                                      readonly=False
                                      )
    ac_incoterm_location = fields.Char(string='Incoterm Location',  related='invoice_line_ids.sale_line_ids.order_id.incoterm_location',
                                       store=True,
                                       readonly=False)

    ac_vessel_name = fields.Char(string='Vessel Name',  related='invoice_line_ids.sale_line_ids.order_id.vessel_name',
                                store=True,
                                readonly=False)
    ac_mode_of_transport = fields.Char(string='Mode of Transport',  related='invoice_line_ids.sale_line_ids.order_id.mode_of_transport',
                                      store=True,
                                      readonly=False)

    ac_consignee = fields.Many2one('res.partner', string='Consignee',related="invoice_line_ids.sale_line_ids.order_id.consignee")
    ac_notify = fields.Many2one('res.partner', string='Notify', related="invoice_line_ids.sale_line_ids.order_id.notify",)

    ac_form_invoice_seq = fields.Char(string='Proform Invoice Sequence', readonly=True,
                                   related="invoice_line_ids.sale_line_ids.order_id.form_invoice_seq",)
    no_and_kind_of_backing = fields.Text(string="No. and Kind of Backing")

    any_other_details = fields.Text(string="Any Other Details")
    declaration = fields.Text(string="Declaration")
    ac_picking_out_name = fields.Char(string="Packing List No",)
