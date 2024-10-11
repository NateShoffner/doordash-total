from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel


class GrandTotal(BaseModel):
    unitAmount: int
    currency: str
    decimalPlaces: int
    displayString: str
    sign: bool
    __typename: str


class Business(BaseModel):
    id: str
    name: str
    __typename: str


class Store(BaseModel):
    id: str
    name: str
    business: Business
    phoneNumber: str
    fulfillsOwnDeliveries: bool
    customerArrivedPickupInstructions: Any
    isPriceMatchingEnabled: bool
    priceMatchGuaranteeInfo: Any
    __typename: str


class OriginalPaymentAmount(BaseModel):
    unitAmount: int
    currency: str
    decimalPlaces: int
    displayString: str
    sign: bool
    __typename: str


class CreditAmount(BaseModel):
    unitAmount: int
    currency: str
    decimalPlaces: int
    displayString: str
    sign: bool
    __typename: str


class CancellationPendingRefundInfoItem(BaseModel):
    state: str
    originalPaymentAmount: OriginalPaymentAmount
    creditAmount: CreditAmount
    __typename: str


class GetConsumerOrdersWithDetail(BaseModel):
    id: str
    orderUuid: str
    deliveryUuid: str
    createdAt: str
    submittedAt: str
    cancelledAt: Optional[str]
    fulfilledAt: Optional[str]
    grandTotal: GrandTotal


class Data(BaseModel):
    getConsumerOrdersWithDetails: List[GetConsumerOrdersWithDetail]


class RequestInfo(BaseModel):
    version: int
    requestId: str
    correlationId: str
    ddb: bool


class Extensions(BaseModel):
    requestInfo: RequestInfo


class Model(BaseModel):
    data: Optional[Data] = None
    extensions: Optional[Extensions] = None

def build_payload(offset: int, limit: int) -> dict:
    payload = '{"operationName":"getConsumerOrdersWithDetails","variables":{"offset":' + str(offset) + ',"limit":' + str(limit) + ',"includeCancelled":true,"orderFilterType":"ORDER_FILTER_TYPE_UNSPECIFIED"},"query":"query getConsumerOrdersWithDetails($offset: Int\u0021, $limit: Int\u0021, $includeCancelled: Boolean, $orderFilterType: OrderFilterType) {\\n  getConsumerOrdersWithDetails(\\n    offset: $offset\\n    limit: $limit\\n    includeCancelled: $includeCancelled\\n    orderFilterType: $orderFilterType\\n  ) {\\n    id\\n    orderUuid\\n    deliveryUuid\\n    createdAt\\n    submittedAt\\n    cancelledAt\\n    fulfilledAt\\n    specialInstructions\\n    isConsumerSubscriptionEligible\\n    isGroup\\n    isReorderable\\n    isGift\\n    isPickup\\n    isMerchantShipping\\n    containsAlcohol\\n    fulfillmentType\\n    shoppingProtocol\\n    orderFilterType\\n    cancellationReorderInfo {\\n      parentOrderUuid\\n      parentDeliveryUuid\\n      cancellationReorderType\\n      __typename\\n    }\\n    creator {\\n      ...ConsumerOrderCreatorFragment\\n      __typename\\n    }\\n    deliveryAddress {\\n      id\\n      formattedAddress\\n      __typename\\n    }\\n    orders {\\n      id\\n      creator {\\n        ...ConsumerOrderCreatorFragment\\n        __typename\\n      }\\n      items {\\n        ...ConsumerOrderOrderItemFragment\\n        __typename\\n      }\\n      __typename\\n    }\\n    paymentCard {\\n      ...ConsumerOrderPaymentCardFragment\\n      __typename\\n    }\\n    grandTotal {\\n      unitAmount\\n      currency\\n      decimalPlaces\\n      displayString\\n      sign\\n      __typename\\n    }\\n    likelyOosItems {\\n      menuItemId\\n      name\\n      photoUrl\\n      __typename\\n    }\\n    pollingInterval\\n    store {\\n      id\\n      name\\n      business {\\n        id\\n        name\\n        __typename\\n      }\\n      phoneNumber\\n      fulfillsOwnDeliveries\\n      customerArrivedPickupInstructions\\n      isPriceMatchingEnabled\\n      priceMatchGuaranteeInfo {\\n        headerDisplayString\\n        bodyDisplayString\\n        buttonDisplayString\\n        __typename\\n      }\\n      __typename\\n    }\\n    recurringOrderDetails {\\n      itemNames\\n      consumerId\\n      recurringOrderUpcomingOrderUuid\\n      scheduledDeliveryDate\\n      arrivalTimeDisplayString\\n      storeName\\n      isCancelled\\n      __typename\\n    }\\n    bundleOrderInfo {\\n      ...BundleOrderInfoFragment\\n      __typename\\n    }\\n    cancellationPendingRefundInfo {\\n      state\\n      originalPaymentAmount {\\n        unitAmount\\n        currency\\n        decimalPlaces\\n        displayString\\n        sign\\n        __typename\\n      }\\n      creditAmount {\\n        unitAmount\\n        currency\\n        decimalPlaces\\n        displayString\\n        sign\\n        __typename\\n      }\\n      __typename\\n    }\\n    __typename\\n  }\\n}\\n\\nfragment ConsumerOrderPaymentCardFragment on ConsumerOrderPaymentCard {\\n  id\\n  last4\\n  type\\n  __typename\\n}\\n\\nfragment ConsumerOrderOrderItemFragment on ConsumerOrderOrderItem {\\n  id\\n  name\\n  quantity\\n  specialInstructions\\n  substitutionPreferences\\n  orderItemExtras {\\n    ...ConsumerOrderOrderItemExtraFragment\\n    __typename\\n  }\\n  purchaseQuantity {\\n    ...ConsumerOrderQuantityFragment\\n    __typename\\n  }\\n  fulfillQuantity {\\n    ...ConsumerOrderQuantityFragment\\n    __typename\\n  }\\n  originalItemPrice\\n  purchaseType\\n  __typename\\n}\\n\\nfragment ConsumerOrderOrderItemExtraOptionFields on OrderItemExtraOption {\\n  menuExtraOptionId\\n  name\\n  description\\n  price\\n  quantity\\n  __typename\\n}\\n\\nfragment ConsumerOrderOrderItemExtraOptionFragment on OrderItemExtraOption {\\n  ...ConsumerOrderOrderItemExtraOptionFields\\n  orderItemExtras {\\n    ...ConsumerOrderOrderItemExtraFields\\n    orderItemExtraOptions {\\n      ...ConsumerOrderOrderItemExtraOptionFields\\n      orderItemExtras {\\n        ...ConsumerOrderOrderItemExtraFields\\n        __typename\\n      }\\n      __typename\\n    }\\n    __typename\\n  }\\n  __typename\\n}\\n\\nfragment ConsumerOrderOrderItemExtraFields on OrderItemExtra {\\n  menuItemExtraId\\n  name\\n  __typename\\n}\\n\\nfragment ConsumerOrderOrderItemExtraFragment on OrderItemExtra {\\n  ...ConsumerOrderOrderItemExtraFields\\n  orderItemExtraOptions {\\n    ...ConsumerOrderOrderItemExtraOptionFragment\\n    __typename\\n  }\\n  __typename\\n}\\n\\nfragment ConsumerOrderCreatorFragment on ConsumerOrderCreator {\\n  id\\n  firstName\\n  lastName\\n  __typename\\n}\\n\\nfragment ConsumerOrderQuantityFragment on Quantity {\\n  continuousQuantity {\\n    quantity\\n    unit\\n    __typename\\n  }\\n  discreteQuantity {\\n    quantity\\n    unit\\n    __typename\\n  }\\n  __typename\\n}\\n\\nfragment BundleOrderInfoFragment on BundleOrderInfo {\\n  primaryBundleOrderUuid\\n  primaryBundleOrderId\\n  bundleOrderUuids\\n  bundleOrderConfig {\\n    ...BundleOrderConfigFragment\\n    __typename\\n  }\\n  __typename\\n}\\n\\nfragment BundleOrderConfigFragment on BundleOrderConfig {\\n  bundleType\\n  bundleOrderRole\\n  __typename\\n}\\n"}'

    return payload
