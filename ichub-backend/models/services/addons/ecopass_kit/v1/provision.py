#################################################################################
# Eclipse Tractus-X - Industry Core Hub Backend
#
# Copyright (c) 2025 Contributors to the Eclipse Foundation
#
# See the NOTICE file(s) distributed with this work for additional
# information regarding copyright ownership.
#
# This program and the accompanying materials are made available under the
# terms of the Apache License, Version 2.0 which is available at
# https://www.apache.org/licenses/LICENSE-2.0.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the
# License for the specific language govern in permissions and limitations
# under the License.
#
# SPDX-License-Identifier: Apache-2.0
#################################################################################

import re

from pydantic import BaseModel, Field, field_validator

_SAFE_FIELD_PATTERN = re.compile(r'^[A-Za-z0-9:._-]+$')


class ShareDppRequest(BaseModel):
    """Request model for sharing a Digital Product Passport"""
    dpp_id: str = Field(
        alias="dppId",
        description="The passport ID of the Digital Product Passport to share (format: CX:manufacturerPartId:partInstanceId)"
    )
    business_partner_number: str = Field(
        alias="businessPartnerNumber",
        description="The BPNL of the business partner to share the DPP with"
    )

    @field_validator("dpp_id", "business_partner_number")
    @classmethod
    def no_control_characters(cls, v: str) -> str:
        if not _SAFE_FIELD_PATTERN.match(v):
            raise ValueError("Invalid characters in field")
        return v

    class Config:
        populate_by_name = True


class ShareDppResponse(BaseModel):
    """Response model for DPP sharing operation"""
    dpp_id: str = Field(alias="dppId", description="The passport ID of the shared DPP")
    business_partner_number: str = Field(
        alias="businessPartnerNumber",
        description="The BPNL the DPP was shared with"
    )
    bpn_discovery_registered: bool = Field(
        alias="bpnDiscoveryRegistered",
        description="Whether the manufacturer part ID was successfully registered in BPN Discovery"
    )

    class Config:
        populate_by_name = True
