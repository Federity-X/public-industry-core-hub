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

import pytest
from pydantic import ValidationError

from models.services.addons.ecopass_kit.v1.provision import ShareDppRequest

_VALID_DPP_ID = "CX:partId:instanceId"
_VALID_BPN = "BPNL00000003CRHK"


class TestShareDppRequest:
    """Tests for the ShareDppRequest Pydantic model, including the log-injection validator."""

    # --- valid inputs ---

    def test_valid_dpp_id_format(self):
        """Standard CX:manufacturerPartId:partInstanceId format is accepted."""
        req = ShareDppRequest(dpp_id=_VALID_DPP_ID, business_partner_number=_VALID_BPN)
        assert req.dpp_id == _VALID_DPP_ID
        assert req.business_partner_number == _VALID_BPN

    def test_valid_with_dots_underscores_hyphens(self):
        """Dots, underscores, and hyphens are allowed characters."""
        req = ShareDppRequest(
            dpp_id="CX:part.id-v1:inst_1",
            business_partner_number=_VALID_BPN,
        )
        assert req.dpp_id == "CX:part.id-v1:inst_1"

    def test_alias_based_construction(self):
        """Model can be built from JSON aliases dppId / businessPartnerNumber."""
        req = ShareDppRequest.model_validate(
            {"dppId": _VALID_DPP_ID, "businessPartnerNumber": _VALID_BPN}
        )
        assert req.dpp_id == _VALID_DPP_ID
        assert req.business_partner_number == _VALID_BPN

    def test_serialisation_round_trip(self):
        """model_dump / model_validate round trip preserves all fields."""
        original = ShareDppRequest(dpp_id=_VALID_DPP_ID, business_partner_number=_VALID_BPN)
        restored = ShareDppRequest.model_validate(original.model_dump())
        assert restored == original

    # --- invalid inputs: dpp_id ---

    def test_newline_in_dpp_id_raises(self):
        """Newline in dpp_id must be rejected to prevent log injection."""
        with pytest.raises(ValidationError):
            ShareDppRequest(dpp_id="CX:id\nfake log entry", business_partner_number=_VALID_BPN)

    def test_carriage_return_in_dpp_id_raises(self):
        """Carriage return in dpp_id must be rejected."""
        with pytest.raises(ValidationError):
            ShareDppRequest(dpp_id="CX:id\rfake", business_partner_number=_VALID_BPN)

    def test_space_in_dpp_id_raises(self):
        """Spaces are not part of the CX ID format and must be rejected."""
        with pytest.raises(ValidationError):
            ShareDppRequest(dpp_id="CX:part id:inst", business_partner_number=_VALID_BPN)

    def test_special_chars_in_dpp_id_raises(self):
        """HTML/shell special characters in dpp_id must be rejected."""
        with pytest.raises(ValidationError):
            ShareDppRequest(dpp_id="CX:<script>alert(1)</script>", business_partner_number=_VALID_BPN)

    def test_empty_dpp_id_raises(self):
        """Empty string for dpp_id must be rejected."""
        with pytest.raises(ValidationError):
            ShareDppRequest(dpp_id="", business_partner_number=_VALID_BPN)

    # --- invalid inputs: business_partner_number ---

    def test_newline_in_bpn_raises(self):
        """Newline in business_partner_number must be rejected to prevent log injection."""
        with pytest.raises(ValidationError):
            ShareDppRequest(dpp_id=_VALID_DPP_ID, business_partner_number="BPNL000\ninjected")

    def test_empty_bpn_raises(self):
        """Empty string for business_partner_number must be rejected."""
        with pytest.raises(ValidationError):
            ShareDppRequest(dpp_id=_VALID_DPP_ID, business_partner_number="")
