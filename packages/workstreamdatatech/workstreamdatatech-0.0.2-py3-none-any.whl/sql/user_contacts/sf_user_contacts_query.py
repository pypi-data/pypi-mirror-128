# final contact table to be pushed to sfdc, deduped and with conflicting leads + deleted contacts filtered out
query_string = """
with min_sf_id as (
    select customer_id
         , min(first_sf_account) first_sf_account
    from (select c.id                                                                                  customer_id
               , first_value(c.salesforce_account_id) over (partition by c.id order by a.created_date) first_sf_account
          from workstream_production.customers c
                   left join salesforce.accounts a on c.salesforce_account_id = a.id) a
    group by 1
),
 user_contact as (
    SELECT c.id                customer_id
         , user_id
         , c.name              account_name
         , first_sf_account
         , co.id               company_id
         , co.name             company_name
         , cs.name
         , split_part(cs.name, ' ', 1) first_name
         , regexp_replace(cs.name, '.*?\s', '') rest_of_name
         , cs.phone
         , cs.global_phone_number
         , cs.sms_phone_number
         , u.email
         , u.last_seen
         , cs.status
         , u.created_at        user_created_at
         , cs.created_at       staff_created_at
         , cs.deleted_at
         , cs.id               company_staff_id
         , ca.company_staff_id fk_company_staff_id
         , ca.role
         , ca.onboard_employee
         , ca.all_admin_rights
    from workstream_production.users u
             left join workstream_production.company_staffs cs on u.id = cs.user_id
             left join workstream_production.companies co on cs.company_id = co.id
             left join workstream_production.customers c on c.id = co.customer_id
             left join workstream_production.company_admins ca on ca.company_staff_id = cs.id
             left join min_sf_id a on c.id = a.customer_id
             left join salesforce.leads l on lower(u.email) = lower(l.email)
             left join salesforce.contacts con on lower(u.email) = lower(con.email)
    where c.salesforce_account_id is not null
      and is_support_staff is false
      and u.email is not null
      and cs.deleted_at is null
      and is_support_staff is false
      and lower(u.email) not like '%workstream%'
      and l.is_deleted is not true and con.is_deleted is not true
      and date_trunc('day',u.created_at) = '{execution_date}'
)
   , dedupe as (
    select email
         , string_agg(company_staff_id::text, ',')
         , min(first_sf_account)                                                 salesforce_account_id
         , max(first_name) as                                                    first_name
         , max(rest_of_name) as                                                  rest_of_name
         , string_agg(distinct company_name || ' (' || company_id || ')', ', ')  company_name
         , max(global_phone_number)                                              global_phone_number
         , max(last_seen)                                                        last_seen
         , min(user_created_at)                                                  user_created_at
         , min(status)                                                           status -- this is min bc 'active' will be prioritized over 'disabled'
         , string_agg(company_name || ' (' || company_id || '): ' || role, ', ') roles
         , max(case when onboard_employee = true then 1 else 0 end)              onboard_employee
         , max(case when all_admin_rights = true then 1 else 0 end)              all_admin_rights
    from user_contact
    group by 1
)
    , multiple_email as (
    select 
        email
        , count(1)
    from salesforce.contacts
    where is_deleted is not true
    group by 1 having count(1) > 1
)
select 
     d.email "Email"
     , salesforce_account_id "AccountId"
     , d.first_name "FirstName"
     , d.rest_of_name "LastName"
     , company_name "User_Company_Name__c"
     , global_phone_number "Phone"
     , last_seen "Last_Seen__c"
     , user_created_at "User_Created_Date__c"
     , d.status "User_Status__c"
     , roles "User_Role__c"
     , onboard_employee "User_Onboard_Employee__c"
     , all_admin_rights "User_All_Admin_Rights__c"
from dedupe d
    left join multiple_email mm on d.email = mm.email
    where mm.email is null
limit 10
;
"""