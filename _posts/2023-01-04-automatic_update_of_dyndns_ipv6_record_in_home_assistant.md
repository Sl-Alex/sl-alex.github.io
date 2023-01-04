---
layout: post
title: Automatic update of IPv6 dynamiс DNS record in Home Assistant
description: How to create a universal wrapper for secure functions in ARM TrustZone MCUs.
categories: Automation
tags: HomeAssistant IPv6
author: Sl-Alex
--- 

My Internet provider offers static IP address only to business clients. Unfortunately, dynamic IPv4 address is also not an option, because it's completely hidden behind provider's NAT. Fortunately, there is an option to expose IPv6 host to the outside world:

{% include image.html url="/assets/2023-01-04-automatic_update_of_dyndns_ipv6_record_in_home_assistant/router_ipv6_host_exposure.png" description="Router settings" %}

As you see, I exposed my Home Assistant server and now I can use any dynamic DNS service with IPv6 support and register my domain name. The only problem is that my externally accessible IPv6 address changes over time. Most of dynamic DNS services have a dedicated API that allows you to update your IP address. In this post I'll show you how to automate it in Home Assistant.



Let's start with getting the correct IPv6 address.
In Home Assistant it can be done by adding the [DNS IP](https://www.home-assistant.io/integrations/dnsip) integration. It periodically gets IPv4 and IPv6 addresses from the external service:

{% include image.html url="/assets/2023-01-04-automatic_update_of_dyndns_ipv6_record_in_home_assistant/dns_ip.png" description="DNS IP integration entities" %}

IPv6 address will be accessible now in ```sensor.myip_ipv6``` entity.

Now let's define a [RESTful Command](https://www.home-assistant.io/integrations/rest_command/) service in our Home Assistant ```configuration.yaml```: 
```yaml
rest_command:
  update_dynv6:
    url: !secret dynv6_auto_update_url
    method: get
```

Please do not store your update URL in the ```configuration.yaml```, because this URL highly likely will contain your API key. The best place would be ```secrets.yaml```:
```yaml
{% raw %}
dynv6_update_url: "https://ipv6.dynv6.com/api/update?hostname=<your.host.name>&token=<your_token>&ipv6={{ ipv6 }}"
dynv6_auto_update_url: "https://ipv6.dynv6.com/api/update?hostname=<your.host.name>&token=<your_token>&ipv6=auto"
{% endraw %}
```

Note that I created two URLs: one for manual update (when our server reports its IPv6 address) and second one for automatic update, when dynamic DNS service will determine IPv6 address of our server automatically.
You can use either approach, I'd recommend using the automatic update if supported by your dynamic DNS service.

Now let's create an automation that will call our RESTful command:

{% include image.html url="/assets/2023-01-04-automatic_update_of_dyndns_ipv6_record_in_home_assistant/automation.png" description="Automation" %}

If you use the automatic IPv6 detection then that's it. If your dynamic DNS service does not have this option then you need to provide the IPv6 address to the template by changing the YAML for the action:
```yaml
{% raw %}
service: rest_command.update_dynv6
data:
  ipv6: "{{ states('sensor.myip_ipv6') }}"
{% endraw %}
```
