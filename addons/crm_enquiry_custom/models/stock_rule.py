# -*- coding: utf-8 -*-

from odoo import models
import logging

_logger = logging.getLogger(__name__)

# ANSI Color codes
WHITE = "\033[97m"
BLUE = "\033[94m"
RESET = "\033[0m"


class StockRule(models.Model):
    _inherit = 'stock.rule'

    def _should_auto_confirm_procurement_mo(self, production):
        """
        Override to prevent auto-confirmation of MRP orders created from sale orders.
        This allows manual review of manufacturing orders before confirmation.
        """
        # Check if production is linked to a sale order
        sale_order = self._find_related_sale_order(production)

        if sale_order:
            _logger.info(
                f"{WHITE}MRP Auto-Confirm Prevention:{RESET} "
                f"{BLUE}MRP [{production.name}]{RESET} linked to "
                f"{BLUE}Sale Order [{sale_order.name}]{RESET} - "
                f"{WHITE}State will remain DRAFT for manual review{RESET}"
            )
            return False

        # Otherwise, use standard behavior
        return super(StockRule, self)._should_auto_confirm_procurement_mo(production)

    def _find_related_sale_order(self, production):
        """
        Find sale order related to the manufacturing order.
        Returns sale.order record or False.
        """
        # Method 1: Search by origin (direct match)
        if production.origin:
            sale_order = self.env['sale.order'].search([('name', '=', production.origin)], limit=1)
            if sale_order:
                return sale_order

        # Method 2: Search by procurement group
        if production.procurement_group_id:
            sale_order = self.env['sale.order'].search([
                ('procurement_group_id', '=', production.procurement_group_id.id)
            ], limit=1)
            if sale_order:
                return sale_order

        # Method 3: Parse origin for sale order reference (multi-line case)
        if production.origin:
            origin_parts = production.origin.split(',')
            for part in origin_parts:
                part = part.strip()
                sale_order = self.env['sale.order'].search([
                    ('name', '=', part)
                ], limit=1)
                if sale_order:
                    return sale_order

        return False
