package helpspotgo

type VersionInfo struct {
	Version    string `json:"version"`
	MinVersion string `json:"min_version"`
}

type VersionResponse struct {
	Version    string `json:"version"`
	MinVersion string `json:"min_version"`
}

type ErrorResponse struct {
	Errors []ErrorItem `json:"errors"`
}

type ErrorItem struct {
	ID          int    `json:"id"`
	Description string `json:"description"`
}

type KBBooksResponse struct {
	Books []KBBook `json:"book"`
}

type RequestsResponse struct {
	Requests []Request `json:"request"`
}

type Response struct {
	Version       VersionResponse `json:"version"`
	Requests      []Request       `json:"requests"`
	Request       Request         `json:"request"`
	Categories    []Category      `json:"categories"`
	CustomFields  []CustomField   `json:"customfields"`
	KBBooks       []KBBook        `json:"-"`
	KBBook        KBBook          `json:"book"`
	KBPage        KBPage          `json:"page"`
	KBSearch      []KBPage        `json:"page"`
	Forums        []Forum         `json:"forums"`
	Forum         Forum           `json:"forum"`
	Topics        []Topic         `json:"topics"`
	Topic         Topic           `json:"topic"`
	Posts         []Post          `json:"posts"`
	Mailboxes     []Mailbox       `json:"mailboxes"`
	StatusTypes   []StatusType    `json:"statusTypes"`
	Staff         []Staff         `json:"activeStaff"`
	Filters       []Filter        `json:"filters"`
	FilterColumns []string        `json:"columnNames"`
	Preferences   map[string]any  `json:"preferences"`
	FieldLabels   map[string]any  `json:"fieldLabels"`
	Raw           string          `json:"-"`
}

type Request struct {
	XRequest         string `json:"xRequest"`
	AccessKey        string `json:"accesskey"`
	Title            string `json:"sTitle"`
	Note             string `json:"tNote"`
	FirstName        string `json:"sFirstName"`
	LastName         string `json:"sLastName"`
	Email            string `json:"sEmail"`
	Phone            string `json:"sPhone"`
	UserID           string `json:"sUserId"`
	Category         string `json:"sCategory"`
	XCategory        string `json:"xCategory"`
	Status           string `json:"sStatus"`
	XStatus          string `json:"xStatus"`
	Urgent           string `json:"fUrgent"`
	Open             string `json:"fOpen"`
	OpenedVia        string `json:"fOpenedVia"`
	OpenedViaID      string `json:"xOpenedViaId"`
	PersonAssignedTo string `json:"xPersonAssignedTo"`
	PersonOpenedBy   string `json:"xPersonOpenedBy"`
	FullName         string `json:"fullname"`
	Created          string `json:"dtGMTOpened"`
	Updated          string `json:"dtGMTChange"`
}

type Category struct {
	XCategory       int    `json:"xCategory"`
	Category        string `json:"sCategory"`
	CustomFieldList []int  `json:"sCustomFieldList"`
}

type CustomField struct {
	XCustomField  int      `json:"xCustomField"`
	FieldName     string   `json:"fieldName"`
	FieldType     string   `json:"fieldType"`
	IsRequired    bool     `json:"isRequired"`
	TextSize      string   `json:"sTxtSize"`
	LargeTextRows string   `json:"lrgTextRows"`
	ListItems     []string `json:"listItems"`
	DecimalPlaces int      `json:"iDecimalPlaces"`
	Regex         string   `json:"sRegex"`
	AlwaysVisible bool     `json:"isAlwaysVisible"`
	Order         int      `json:"iOrder"`
}

type KBBook struct {
	XKBBook string   `json:"xBook"`
	Title   string   `json:"sBookName"`
	Pages   []KBPage `json:"pages,omitempty"`
}

type KBPage struct {
	XKBPage   int    `json:"xKBPage"`
	XKBBook   int    `json:"xKBBook"`
	Title     string `json:"sTitle"`
	Content   string `json:"tContent"`
	PageOrder int    `json:"iPageOrder"`
}

type Forum struct {
	XForum   int    `json:"xForum"`
	Title    string `json:"sTitle"`
	Topics   int    `json:"iTopics"`
	Posts    int    `json:"iPosts"`
	LastPost int    `json:"dtGMTLastPost"`
}

type Topic struct {
	XTopic   int    `json:"xTopic"`
	XForum   int    `json:"xForum"`
	Title    string `json:"sTitle"`
	Author   string `json:"sAuthor"`
	Posts    int    `json:"iPosts"`
	Views    int    `json:"iViews"`
	LastPost int    `json:"dtGMTLastPost"`
	Sticky   bool   `json:"fSticky"`
	Locked   bool   `json:"fLocked"`
}

type Post struct {
	XPost   int    `json:"xPost"`
	XTopic  int    `json:"xTopic"`
	Content string `json:"tPost"`
	Author  string `json:"sAuthor"`
	Created int    `json:"dtGMTCreated"`
}

type Mailbox struct {
	XMailbox int    `json:"xMailbox"`
	Name     string `json:"sName"`
	Email    string `json:"sEmail"`
}

type StatusType struct {
	XStatus int    `json:"xStatus"`
	Status  string `json:"sStatus"`
	IsOpen  bool   `json:"fOpen"`
	Order   int    `json:"iOrder"`
}

type Staff struct {
	XPerson int    `json:"xPerson"`
	Name    string `json:"sName"`
	Email   string `json:"sEmail"`
}

type Filter struct {
	XFilter int    `json:"xFilter"`
	Name    string `json:"sName"`
	Columns string `json:"sColumns"`
	Query   string `json:"sQuery"`
	Public  bool   `json:"fPublic"`
	UserID  int    `json:"xUser"`
}
