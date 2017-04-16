For start EbiLock emulator IUT version, make config .json file, and run command: 

java -jar ebi-emulator-0.2.3.jar 9090 9091 emulator_config.json

java -jar file.jar [listen port1] [listen port2] [config.json]

===========================
JSON example: 

[
  {
    "Telegrams": [
      { "ocAddr": "0x3257", "TelegramRules": [""], "Zones": [0,1,2,3] },
      { "ocAddr": "0x3258", "TelegramRules": [""], "Zones": [0,1,2,3] }
    ],
    "Repeat": 6,
    "PackageRules": [""]
  },
  {
    "Telegrams": [
      { "ocAddr": "0x3257", "TelegramRules": ["SET_WRONG_A_CRC8"], "Zones": [0,1,2,3] },
      { "ocAddr": "0x3258", "TelegramRules": null, "Zones": [0,1,2,3] }
    ],
    "Repeat": 6,
    "PackageRules": null
  },
  {
    "Telegrams": [
      { "ocAddr": "0x3257", "TelegramRules": [""], "Zones": [0,1,2,3] },
      { "ocAddr": "0x3258", "TelegramRules": [""], "Zones": [0,1,2,3] }
    ],
    "Repeat": 0,
    "PackageRules": ["SEND_EMPTY_ORDER"]
  }
]

=========================== 

ocAddr	-	address for Object Controller in hex format
Zones 	-	zone statuses: 0-error, 1-clear, 2-work, 3-error
Repeat	-	how many times repeat this package

===========================
Telegram Rules:
    SET_WRONG_A_CRC8	- Set wrong CRC8 for telegram A
    SET_WRONG_B_CRC8	- Set wrong CRC8 for telegram B
    SET_CYCLE_AB_PLUS1	- Set CYCLE A+1 B-1
    SET_ML_A_0		- Set telegram A LENGTH as 0 (ML=0x05)
    SET_ML_B_0		- Set telegram B LENGTH as 0 (ML=0x05)
    SET_NULL_DATA_A	- Set empty DATA for telegram A
    SET_NULL_DATA_B	- Set empty DATA for telegram B
    SET_ML_A_NULL	- Set telegram A LENGTH as NULL (ML=0x00)
    SET_ML_B_NULL	- Set telegram B LENGTH as NULL (ML=0x00)
    SET_CO_A_STATUS	- Set TYPE telegram A = status
    SET_CO_B_STATUS	- Set TYPE telegram B = status
    SET_DOUBLE_TELEGRAM_AB	- Set double telegrams AB
    SET_DOUBLE_TELEGRAM_AB_V2	- Set double telegrams AB Version2

===========================
Package Rules:
    PUSH_BY_ONE_BYTE		- Push data in the socket by one byte  // for all other rules

    SEND_STATUS_TELEGRAM	- Send_STATUS_telegram(!!!)  // not changed by other rules
    SEND_EMPTY_ORDER		- Send empty odrder, without body  // not changed by other rules
    SEND_GARBAGE_HDLC		- Send garbage instead of normal data  // not changed by other rules
    SEND_GARBAGE_HDLC_SIZED	- Send garbage sized by _LIMIT instead of normal data  // not changed by other rules
    SEND_GARBAGE_OVERSIZED_HDLC	- Send oversized(_LIMIT+1) garbage HDLC  // not changed by other rules
    SEND_GARBAGE_DOUBLESIZED_HDLC	- Send DOUBLESIZED garbage HDLC  // not changed by other rules
    SEND_GARBAGE_THIRDSIZED_HDLC	- Send THIRDSIZED garbage HDLC  // not changed by other rules
    SEND_GARBAGE_FOURTHSIZED_HDLC	- Send FOURTHSIZED garbage HDLC  // not changed by other rules
    SEND_HDLC_DOUBLESIZED	- Send DOUBLESIZED hdlc // not changed by other rules
    SEND_HDLC_THIRDSIZED	- Send THIRDSIZED hdlc // not changed by other rules
    SEND_HDLC_FOURTHSIZED	- Send FOURTHSIZED hdlc // not changed by other rules
    SEND_TWO_HDLC_IN_PACKAGE	- Send TWO hdlc telegrams with NOT increased counters in 1 package // not changed by other rules
    SEND_FOUR_HDLC_IN_PACKAGE	- Send FOUR hdlc telegrams with NOT increased counters in 1 package // not changed by other rules

    SET_PACKAGE_WRONG_CRC16	- Set wrong_CRC16_sum 
    SET_PACKAGE_FROM_CLIENT	- Set package_FROM_client 
    SET_PACKAGE_TO_IPU		- Set package_TO_ipu 
    SET_PACKAGE_TYPE_2		- Set package_TYPE_as Order 
    SET_PACKAGE_TYPE_3		- Set package_TYPE_as Status 
    SET_PACKAGE_TYPE_4		- Set package_TYPE_as Empty order 
    SET_PACKAGE_TYPE_5		- Set package_TYPE_as Data between OCs 
    SET_PACKAGE_WRONG_LENGTH	- Set package_LENGTH_not as body length 
    SET_PACKAGE_NULL_LENGTH	- Set package_LENGTH_as 0x00 
    SET_PACKAGE_NULL_BODY	- Set_BODY_as Empty 

    SET_TM_WRONG_CYCLE_A	- Set wrong_CYCLE_telegram A 
    SET_TM_WRONG_CYCLE_B	- Set wrong_CYCLE_telegram B 
    SET_TM_CYCLE_AB_PLUS1	- Set_CYCLE_A+1,B-1 
    SET_TM_CYCLE_AB_PLUS2	- Set_CYCLE_A+2,B-2 
    SET_TM_WRONG_HEADER_BLOCK_SIZE
    SET_TM_NULL_HEADER_BLOCK_SIZE
    SET_TM_EMPTY_BODY_SIZE
    SET_TM_DOUBLE_BODY		- Repeat body twice, with same data and counters
