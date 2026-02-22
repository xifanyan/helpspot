package helpspotgo

import (
	"fmt"
	"io"
	"os"
	"sync"
	"time"
)

type Level int

const (
	Debug Level = iota
	Info
	Warn
	Error
)

var (
	levelNames = map[Level]string{
		Debug: "DEBUG",
		Info:  "INFO",
		Warn:  "WARN",
		Error: "ERROR",
	}
	defaultLevel = Warn
)

type Logger struct {
	mu     sync.Mutex
	writer io.Writer
	level  Level
	debug  bool
}

var globalLogger = &Logger{
	writer: os.Stderr,
	level:  defaultLevel,
	debug:  false,
}

func SetDebug(enabled bool) {
	globalLogger.mu.Lock()
	defer globalLogger.mu.Unlock()
	globalLogger.debug = enabled
	if enabled {
		globalLogger.level = Debug
	} else {
		globalLogger.level = defaultLevel
	}
}

func SetWriter(w io.Writer) {
	globalLogger.mu.Lock()
	defer globalLogger.mu.Unlock()
	globalLogger.writer = w
}

func LogDebug(format string, args ...interface{}) {
	globalLogger.log(Debug, format, args...)
}

func LogInfo(format string, args ...interface{}) {
	globalLogger.log(Info, format, args...)
}

func LogWarn(format string, args ...interface{}) {
	globalLogger.log(Warn, format, args...)
}

func LogError(format string, args ...interface{}) {
	globalLogger.log(Error, format, args...)
}

func (l *Logger) log(level Level, format string, args ...interface{}) {
	l.mu.Lock()
	defer l.mu.Unlock()

	if level < l.level {
		return
	}

	timestamp := time.Now().Format("2006-01-02 15:04:05")
	levelStr := levelNames[level]
	msg := fmt.Sprintf(format, args...)

	fmt.Fprintf(l.writer, "%s [%s] %s\n", timestamp, levelStr, msg)
}
