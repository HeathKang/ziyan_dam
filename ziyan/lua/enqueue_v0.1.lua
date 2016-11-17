
--[[

for AK, Vision, OPC, DB ...

]]
-- key1,argv1,argv2,argv3,argv4
-- KEYS[1], equipment
-- ARGV[1], new status value
-- ARGV[2], timestamp
-- ARGV[3], message 
-- ARGV[4], ttl

-- eqpt_no,timestamp, cmd, measurement, data, rawdata

local old_status = 1

local eqpt_no = KEYS[1]
local timestamp = ARGV[1]

local rawdata =ARGV[5]

-- key = eqpt_no & node name
local eqpt_key = string.format("%s_%s", KEYS[1], ARGV[2])

local old_value = redis.call("HGET", eqpt_key,"val")

-- redis.call("HSET", eqpt_key,"timestamp",timestamp)

local old_timestamp = redis.call("HGET", eqpt_key,"timestamp")

-- return old_timestamp

if old_timestamp == false then
    redis.call("HSET", eqpt_key,"timestamp",timestamp)
     old_timestamp = redis.call("HGET", eqpt_key,"timestamp")
    -- return old_timestamp
end
    
local mark = 0
    
if timestamp - old_timestamp > 1500 then
    mark = 1
end

local tag = nil

if old_value == false then
    redis.call("HSET", eqpt_key,"val",rawdata )
elseif old_value == rawdata  and mark == 0 then
    return "same"
else
    if mark == 1 then
        tag = 'hb'
    end
    
    mark = 0
    redis.call("HSET", eqpt_key,"val",rawdata )
    redis.call("HSET", eqpt_key,"timestamp",timestamp)

    local vdata =cmsgpack.unpack(ARGV[4])

    local cmd = ARGV[2]

    local s = {    
            cmd = ARGV[2], 
            rawdata = rawdata,        
            data = {  
                measurement = ARGV[3],
                time = ARGV[1],        
                fields = {data = vdata[1]},        
                tags = {eqpt_no =  KEYS[1], node = "n3"}
            }
        }



    local msg = cmsgpack.pack(s)

    redis.call("RPUSH", "data_queue",msg) -- msg queue    
    redis.call("PUBLISH", "new_data", "new") -- notice    
    
    
    return old_value
    
end



