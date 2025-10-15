---
name: Connector request
about: Request a new API connector template
title: '[CONNECTOR] '
labels: connector, enhancement
assignees: ''

---

**API Provider**
Name of the API you want a connector for (e.g., "Stripe", "OpenAI", "Twilio")

**API Documentation**
Link to the API documentation: 

**Use Case**
What would you use this connector for?

**Priority Endpoints**
Which API endpoints do you need? (List 3-5 most important)
1. 
2. 
3. 

**Authentication**
What authentication method does this API use?
- [ ] API Key (header)
- [ ] API Key (query param)
- [ ] Bearer token
- [ ] OAuth2
- [ ] Basic Auth
- [ ] Other: 

**Rate Limits**
Does the API have rate limits? If so, what are they?

**Cost Structure**
Is this a paid API? What's the pricing model?
- [ ] Free
- [ ] Freemium (with limits)
- [ ] Pay-per-use
- [ ] Subscription

**Example Request**
```bash
# Paste an example curl request (remove sensitive data!)
curl https://api.example.com/endpoint \
  -H "Authorization: Bearer XXX"
```

**Example Response**
```json
{
  "example": "response"
}
```

**Additional Notes**
Any other important information about this API?

**Would you be willing to contribute this connector?**
- [ ] Yes, I can create the YAML config
- [ ] Yes, with a template/example
- [ ] No, but I can test it
- [ ] No, just requesting

