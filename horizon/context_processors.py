# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2012 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
#
# Copyright 2012 Nebula, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
"""
Context processors used by Horizon.
"""

import logging

from django.conf import settings


LOG = logging.getLogger(__name__)


def horizon(request):
    """ The main Horizon context processor. Required for Horizon to function.

    The following variables are added to the request context:

    ``authorized_tenants``
        A list of tenant objects which the current user has access to.

    ``regions``

        A dictionary containing information about region support, the current
        region, and available regions.

    Additionally, it sets the names ``True`` and ``False`` in the context
    to their boolean equivalents for convenience.

    .. warning::

        Don't put API calls in context processors; they will be called once
        for each template/template fragment which takes context that is used
        to render the complete output.
    """
    context = {"HORIZON_CONFIG": getattr(settings, "HORIZON_CONFIG", {}),
               "True": True,
               "False": False}

    # Auth/Keystone context
    context.setdefault('authorized_tenants', [])
    current_dash = request.horizon['dashboard']
    needs_tenants = getattr(current_dash, 'supports_tenants', False)
    if request.user.is_authenticated() and needs_tenants:
        context['authorized_tenants'] = request.user.authorized_tenants

    # Region context/support
    available_regions = getattr(settings, 'AVAILABLE_REGIONS', [])
    regions = {'support': len(available_regions) > 1,
               'current': {'endpoint': request.session.get('region_endpoint'),
                           'name': request.session.get('region_name')},
               'available': [{'endpoint': region[0], 'name':region[1]} for
                             region in available_regions]}
    context['regions'] = regions

    return context
