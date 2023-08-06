import pytest
import json


PAYLOAD = {
    "id": "evt_1I0SkiGeGvgK89lRJLGcWcdq",
    "object": "event",
    "api_version": "2020-08-27",
    "created": 1608473956,
    "data": {
        "object": {
            "id": "in_1I0SjpGeGvgK89lRLJThS7KK",
            "object": "invoice",
            "account_country": "ES",
            "account_name": "BLABLA",
            "account_tax_ids": None,
            "amount_due": 4000,
            "amount_paid": 4000,
            "amount_remaining": 0,
            "application_fee_amount": None,
            "attempt_count": 1,
            "attempted": True,
            "auto_advance": False,
            "billing_reason": "subscription_create",
            "charge": "ch_1I0SkhGeGvgK89lR2sGeIYZk",
            "collection_method": "charge_automatically",
            "created": 1608473901,
            "currency": "eur",
            "custom_fields": None,
            "customer": "cus_Ibg5fE2K1XzMCI",
            "customer_address": None,
            "customer_email": "test@test.com",
            "customer_name": None,
            "customer_phone": None,
            "customer_shipping": None,
            "customer_tax_exempt": "none",
            "customer_tax_ids": [],
            "default_payment_method": None,
            "default_source": None,
            "default_tax_rates": [],
            "description": None,
            "discount": None,
            "discounts": [],
            "due_date": None,
            "ending_balance": 0,
            "footer": None,
            "hosted_invoice_url": "https://invoice.stripe.com/i/acct_1ALBplGeGvgK89lR/invst_Ibg6zwbCjxVMacznqYPWJnva41oKtDF",
            "invoice_pdf": "https://pay.stripe.com/invoice/acct_1ALBplGeGvgK89lR/invst_Ibg6zwbCjxVMacznqYPWJnva41oKtDF/pdf",
            "last_finalization_error": None,
            "lines": {
                "object": "list",
                "data": [
                    {
                        "id": "il_1I0SjpGeGvgK89lRpkXE3p4M",
                        "object": "line_item",
                        "amount": 4000,
                        "currency": "eur",
                        "description": "1 × Subscripció TESTING (at €40.00 / year)",
                        "discount_amounts": [],
                        "discountable": True,
                        "discounts": [],
                        "livemode": False,
                        "metadata": {
                            "path": "/guillotina/subscription",
                            "db": "db"
                        },
                        "period": {
                            "end": 1640009901,
                            "start": 1608473901
                        },
                        "plan": {
                            "id": "price_1HNb9XGeGvgK89lRkF3KPEgs",
                            "object": "plan",
                            "active": True,
                            "aggregate_usage": None,
                            "amount": 4000,
                            "amount_decimal": "4000",
                            "billing_scheme": "per_unit",
                            "created": 1599211455,
                            "currency": "eur",
                            "interval": "year",
                            "interval_count": 1,
                            "livemode": False,
                            "metadata": {},
                            "nickname": None,
                            "product": "prod_HxWBZBSRA1ZV1H",
                            "tiers_mode": None,
                            "transform_usage": None,
                            "trial_period_days": None,
                            "usage_type": "licensed"
                        },
                        "price": {
                            "id": "price_1HNb9XGeGvgK89lRkF3KPEgs",
                            "object": "price",
                            "active": True,
                            "billing_scheme": "per_unit",
                            "created": 1599211455,
                            "currency": "eur",
                            "livemode": False,
                            "lookup_key": None,
                            "metadata": {},
                            "nickname": None,
                            "product": "prod_HxWBZBSRA1ZV1H",
                            "recurring": {
                                "aggregate_usage": None,
                                "interval": "year",
                                "interval_count": 1,
                                "trial_period_days": None,
                                "usage_type": "licensed"
                            },
                            "tiers_mode": None,
                            "transform_quantity": None,
                            "type": "recurring",
                            "unit_amount": 4000,
                            "unit_amount_decimal": "4000"
                        },
                        "proration": False,
                        "quantity": 1,
                        "subscription": "sub_Ibg6j4TZGkDH3d",
                        "subscription_item": "si_Ibg6YxvR24GDQu",
                        "tax_amounts": [],
                        "tax_rates": [],
                        "type": "subscription"
                    }
                ],
                "has_more": False,
                "total_count": 1,
                "url": "/v1/invoices/in_1I0SjpGeGvgK89lRLJThS7KK/lines"
            },
            "livemode": False,
            "next_payment_attempt": None,
            "number": "DD59E763-0001",
            "paid": True,
            "payment_intent": "pi_1I0SjpGeGvgK89lRRpzTMumY",
            "period_end": 1608473901,
            "period_start": 1608473901,
            "post_payment_credit_notes_amount": 0,
            "pre_payment_credit_notes_amount": 0,
            "receipt_number": None,
            "starting_balance": 0,
            "statement_descriptor": None,
            "status": "paid",
            "status_transitions": {
                "finalized_at": 1608473901,
                "marked_uncollectible_at": None,
                "paid_at": 1608473955,
                "voided_at": None
            },
            "subscription": "sub_Ibg6j4TZGkDH3d",
            "subtotal": 4000,
            "tax": None,
            "total": 4000,
            "total_discount_amounts": [],
            "total_tax_amounts": [],
            "transfer_data": None,
            "webhooks_delivered_at": None
        }
    },
    "livemode": False,
    "pending_webhooks": 1,
    "request": {
        "id": None,
        "idempotency_key": "pi_1I0SjpGeGvgK89lRRpzTMumY-src_1I0SjqGeGvgK89lRNMDOYVAt"
    },
    "type": "invoice.paid"
}

@pytest.mark.asyncio
async def test_pay_subscription_us(container_requester):
    async with container_requester as requester:
        resp, status_code = await requester(
            "POST",
            "/db/guillotina/",
            data=json.dumps({"@type": "CustomSubscriptionType", "id": "subscription"}),
        )

        assert status_code == 201

        resp, status_code = await requester(
            "GET",
            "/db/guillotina/subscription/@subscriptions",
        )

        resp['error'] == 'No customer'

        resp, status_code = await requester(
            "GET",
            "/db/guillotina/subscription/@cards",
        )

        assert status_code == 200
        assert len(resp['data']) == 0

        resp, status_code = await requester(
            "POST",
            "/db/guillotina/subscription/@register-card",
            data=json.dumps({
                "email": "test@test.com",
                "number": "4242424242424242",
                "expMonth": "12",
                "expYear": "2030",
                "cvc": "123",
                "cardholderName": "Test user",
                "address": "C\ Carrer 99",
                "state": "Barcelona",
                "city": "Barcelona",
                "cp": "08000",
                "country": "ES",
                "phone": "000000000"
            })
        )

        pmid = resp['id']

        resp, status_code = await requester(
            "GET",
            "/db/guillotina/subscription/@cards",
        )

        assert status_code == 200
        assert len(resp['data']) == 1

        resp, status_code = await requester(
            "POST",
            "/db/guillotina/subscription/@subscribe",
            data=json.dumps({
                'pmid': pmid
            })
        )

        assert resp['status'] == 'active'

        resp, status_code = await requester(
            "GET",
            "/db/guillotina/subscription"
        )

        assert resp['subscribed'] is True

        
@pytest.mark.asyncio
async def test_pay_subscription_eu(container_requester):
    async with container_requester as requester:
        resp, status_code = await requester(
            "POST",
            "/db/guillotina/",
            data=json.dumps({"@type": "CustomSubscriptionType", "id": "subscription"}),
        )

        assert status_code == 201

        resp, status_code = await requester(
            "POST",
            "/db/guillotina/subscription/@register-card",
            data=json.dumps({
                "email": "test@test.com",
                "number": "4000002760003184",
                "expMonth": "12",
                "expYear": "2030",
                "cvc": "123",
                "cardholderName": "Test user",
                "address": "C\ Carrer 99",
                "state": "Barcelona",
                "city": "Barcelona",
                "cp": "08000",
                "country": "ES",
                "phone": "000000000"
            })
        )

        pmid = resp['id']

        resp, status_code = await requester(
            "GET",
            "/db/guillotina/subscription/@cards",
        )

        assert status_code == 200
        assert len(resp['data']) == 1

        resp, status_code = await requester(
            "POST",
            "/db/guillotina/subscription/@subscribe",
            data=json.dumps({
                'pmid': pmid
            })
        )

        assert resp['status'] == 'incomplete'
        action = resp['latest_invoice']['payment_intent']['next_action'] 
        assert action['type'] == 'use_stripe_sdk'
        assert action['use_stripe_sdk']['type'] == 'three_d_secure_redirect'

        resp, status_code = await requester(
            "POST",
            "/@stripe",
            data=json.dumps(PAYLOAD)
        )

        assert resp['status'] == 'success'

        resp, status_code = await requester(
            "GET",
            "/db/guillotina/subscription",
        )

        assert resp['subscribed'] == True
