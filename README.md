# Overview

This layer provides the base layer for OpenStack charms that are intended for
use as principle (rather than subordinate) charms; to use this layer add:

    include: ['layer:openstack-principle']

to the layer.yaml in your charm.

For charms hosting OpenStack API services, you probably want to use the
[openstack-api](https://github.com/openstack/charm-layer-openstack-api)
layer instead of this layer
