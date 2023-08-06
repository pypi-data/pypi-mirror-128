# -*- coding: utf-8 -*-
# Copyright © 2021 Wacom. All rights reserved.
from typing import Dict, List, Any, Tuple, Union
import enum

import requests
from requests import Response

from knowledge.services.base import WacomServiceAPIClient, WacomServiceException


# -------------------------------------- Constant flags ----------------------------------------------------------------
TENANT_ID: str = 'tenantId'
USER_ID_TAG: str = 'userId'
LIMIT_TAG: str = 'limit'
OFFSET_TAG: str = 'offset'
ROLES_TAG: str = 'roles'
META_DATA_TAG: str = 'metaData'
INTERNAL_USER_ID_TAG: str = 'internalUserId'
EXTERNAL_USER_ID_TAG: str = 'externalUserId'
CONTENT_TYPE_FLAG: str = 'Content-Type'
TENANT_API_KEY_FLAG: str = 'x-tenant-api-key'


class UserRole(enum.Enum):
    """
    UserRole
    --------
    Roles of the users in
    """
    USER = 'User'
    """User only has control over his personal entities."""
    ADMIN = 'TenantAdmin'
    """TenantAdmin has access to all entities independent of the access rights."""


USER_ROLE_MAPPING: Dict[str, UserRole] = dict([(r.value, r) for r in UserRole])


class UserManagementServiceAPI(WacomServiceAPIClient):
    """
    User-Management Service API
    -----------------------------

    Functionality:
        - List all users
        - Create / update / delete users

    Parameters
    ----------
    service_url: str
        URL of the service
    service_endpoint: str
        Base endpoint
    """

    USER_DETAILS_ENDPOINT: str = f'{WacomServiceAPIClient.USER_ENDPOINT}/internal-id'
    SERVICE_URL: str = 'https://semantic-ink-private.wacom.com'

    def __init__(self, service_url: str = SERVICE_URL, service_endpoint: str = 'graphdata'):
        super().__init__("GroupManagementServiceAPI", service_url=service_url, service_endpoint=service_endpoint)

    # ------------------------------------------ Users handling --------------------------------------------------------

    def create_user(self, tenant_key: str, external_id: str, meta_data: Dict[str, str] = None,
                    roles: List[UserRole] = None) -> Tuple[str, str, str, Dict[str, Any], List[UserRole]]:
        """
        Creates user for a tenant.

        Parameters
        ----------
        tenant_key: str -
            API key for tenant
        external_id: str -
            External id of user identification service.
        meta_data: Dict[str, str]
            Meta-data dictionary.
        roles: List[UserRole]
            List of roles.

        Returns
        -------
        user_id: str
            User  Id
        tenant_id: str
            Tenant Id
        external_user_id: str
            External user Id
        meta_data: Dict[str, Any]
            Meta data for user.
        roles: List[UserRole]
            List of roles.

        Raises
        ------
        WacomServiceException
            If the tenant service returns an error code.
        """
        url: str = f'{self.service_base_url}{UserManagementServiceAPI.USER_ENDPOINT}'
        headers: dict = {
            TENANT_API_KEY_FLAG: tenant_key,
            CONTENT_TYPE_FLAG: 'application/json'
        }
        payload: dict = {
            EXTERNAL_USER_ID_TAG: external_id,
            META_DATA_TAG: meta_data if meta_data is not None else {},
            ROLES_TAG: [r.value for r in roles] if roles is not None else [UserRole.USER.value]
        }
        response: Response = requests.post(url, headers=headers, json=payload, verify=self.verify_calls)
        if response.ok:
            results: Dict[str, Union[str, Dict[str, str], List[str]]] = response.json()
            user_id: str = results['id']
            tenant_id: str = results['tenantId']
            external_user_id: str = results['externalUserId']
            meta_data: Dict[str, Any] = results['metaData']
            user_roles: List[UserRole] = [USER_ROLE_MAPPING[r] for r in results['roles']]
            return user_id, tenant_id, external_user_id, meta_data, user_roles

        raise WacomServiceException(f'Response code:={response.status_code}, exception:= {response.text}')

    def update_user(self, tenant_key: str, internal_id: str, external_id: str, meta_data: Dict[str, str] = None,
                    roles: List[UserRole] = None):
        """Updates user for a tenant.

        Parameters
        ----------
        tenant_key: str
            API key for tenant
        internal_id: str
            Internal id of semantic service.
        external_id: str
            External id of user identification service.
        meta_data: Dict[str, str]
            Meta-data dictionary.
        roles: List[UserRole]
            List of roles.

        Raises
        ------
        WacomServiceException
            If the tenant service returns an error code.
        """
        url: str = f'{self.service_base_url}{UserManagementServiceAPI.USER_ENDPOINT}'
        headers: Dict[str, str] = {
            TENANT_API_KEY_FLAG: tenant_key,
            CONTENT_TYPE_FLAG: 'application/json'
        }
        payload: Dict[str, str] = {
            META_DATA_TAG: meta_data if meta_data is not None else {},
            ROLES_TAG: [r.value for r in roles] if roles is not None else [UserRole.USER.value]
        }
        params: Dict[str, str] = {
            USER_ID_TAG: internal_id,
            EXTERNAL_USER_ID_TAG: external_id
        }
        response: Response = requests.patch(url, headers=headers, json=payload, params=params, verify=self.verify_calls)
        if not response.ok:
            raise WacomServiceException(f'Updating user failed. '
                                        f'Response code:={response.status_code}, exception:= {response.text}')

    def delete_user(self, tenant_key: str, external_id: str, internal_id: str):
        """Deletes user from tenant.

        Parameters
        ----------
        tenant_key: str
            API key for tenant
        external_id: str
            External id of user identification service.
        internal_id: str
            Internal id of user.

        Raises
        ------
        WacomServiceException
            If the tenant service returns an error code.
        """
        url: str = f'{self.service_base_url}{UserManagementServiceAPI.USER_ENDPOINT}'
        headers: Dict[str, str] = {
            TENANT_API_KEY_FLAG: tenant_key
        }
        params: Dict[str, str] = {
            USER_ID_TAG: internal_id,
            EXTERNAL_USER_ID_TAG: external_id
        }
        response: Response = requests.delete(url, headers=headers, params=params, verify=self.verify_calls)
        if not response.ok:
            raise WacomServiceException(f'Response code:={response.status_code}, exception:= {response.text}')

    def user_internal_id(self, tenant_key: str, external_id: str) -> Dict[str, Any]:
        """User internal id.

        Parameters
        ----------
        tenant_key: str
            API key for tenant
        external_id: str
            External id of user

        Returns
        -------
        internal_user_id: str
            Internal id of users

        Raises
        ------
        WacomServiceException
            If the tenant service returns an error code.
        """
        url: str = f'{self.service_base_url}{UserManagementServiceAPI.USER_DETAILS_ENDPOINT}'
        headers: dict = {
            TENANT_API_KEY_FLAG: tenant_key
        }
        parameters: Dict[str, str] = {
            EXTERNAL_USER_ID_TAG:  external_id
        }
        response: Response = requests.get(url, headers=headers, params=parameters, verify=self.verify_calls)
        if response.ok:
            response_dict: Dict[str, Any] = response.json()
            return response_dict[INTERNAL_USER_ID_TAG]
        raise WacomServiceException(f'Response code:={response.status_code}, exception:= {response.text}')

    def listing_users(self, tenant_key: str, offset: int = 0, limit: int = 20)\
            -> List[Tuple[str, str, str, Dict[str, Any], List[UserRole]]]:
        """
        Listing all users configured for this instance.

        Parameters
        ----------
        tenant_key: str
            API key for tenant
        offset: int - [optional]
            Offset value to define starting position in list. [DEFAULT:= 0]
        limit: int - [optional]
            Define the limit of the list size. [DEFAULT:= 20]

        Returns
        -------
        user:  List[Tuple[str, str, str, Dict[str, Any], List[UserRole]]]
            List of users.
        """
        url: str = f'{self.service_url}/{self.service_endpoint}{UserManagementServiceAPI.USER_ENDPOINT}'
        headers: Dict[str, str] = {
            TENANT_API_KEY_FLAG: tenant_key
        }
        params: Dict[str, str] = {
            OFFSET_TAG: offset,
            LIMIT_TAG: limit
        }
        response: Response = requests.get(url, headers=headers, params=params, verify=self.verify_calls)
        if response.ok:
            users: List[Dict[str, Any]] = response.json()
            results: List[Tuple[str, str, str, Dict[str, Any], List[UserRole]]] = []
            for u in users:
                user_id: str = u['id']
                tenant_id: str = u[TENANT_ID]
                external_user_id: str = u['externalUserId']
                meta_data: Dict[str, Any] = u['metaData']
                user_roles: List[UserRole] = [USER_ROLE_MAPPING[r] for r in u['roles']]
                results.append((user_id, tenant_id, external_user_id, meta_data, user_roles))
            return results
        raise WacomServiceException(f'Listing of users failed.'
                                    f'Response code:={response.status_code}, exception:= {response.text}')
