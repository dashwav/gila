/*
If anyone can provide more edge-case designs here that would help
Is this a valid use of an HCL config file?
*/

exists = true
filetype = "hcl"
# Comments in HCL are pound signs AND /* */
meta {
    filename = "hcl_config"
}

contents = [
    {
        name = "exists"
        value_type = "boolean"
        value = true
    },
    {
        name = "filetype"
        value_type = "string"
        value = "hcl"
    }
]