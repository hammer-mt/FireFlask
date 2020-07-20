### 8: Adding Teams and Roles

We now want to add the ability to create a team and invite coworkers or colleagues to that team.

We'll use this blog post as a guide:
https://blog.checklyhq.com/building-a-multi-tenant-saas-data-model/

Here's the general data structure:

- Users can create many Teams.
- Teams can have many Users.
- Users have role-based access to a Team.
- Teams each have their own collection.

Teams
- id
- current_period_ends
- stripe_subscription_id
- stripe_customer_id
- plan
- features []

Memberships
- id
- user_id
- team_id
- role ['READ', 'EDIT', 'ADMIN', 'OWNER']