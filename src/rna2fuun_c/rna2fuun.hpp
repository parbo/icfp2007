#ifndef RNA2FUUN_HPP_
#define RNA2FUUN_HPP_
#include <string>
#include <vector>
#include <map>

typedef struct pixelbuffer {
    int size;
    const char* data;
} pixelbuffer;

struct pixel
{
	unsigned char r;
	unsigned char g;
	unsigned char b;
	unsigned char a;
};

class rna2fuun
{
private:
	int m_x;
	int m_y;
	int m_mx;
	int m_my;
	mutable bool m_cCache;
	mutable pixel m_c;
	mutable bool m_aCache;
	mutable unsigned char m_a;
	mutable bool m_cpCache;
	mutable pixel m_cp;
	int m_dir;
	std::vector<std::vector<pixel> > m_bitmaps;
	std::map<std::string, unsigned int> m_commands;
	std::vector<pixel> m_cbucket;
	std::vector<unsigned char> m_abucket;

public:
	rna2fuun();
	~rna2fuun();

    void reset();    
    void addColor(const pixel& c);   
    void addAlpha(unsigned char a);
    void emptyBucket();
    pixel averageColor(unsigned char def) const;
    unsigned char averageAlpha(unsigned char def) const;
    const pixel& currentPixel() const;
    void move();
	void turnCounterClockwise();
	void turnClockwise();
	pixel& getPixel(unsigned int x, unsigned int y);
    void setPixel(unsigned int x, unsigned int y)
    {
    	getPixel(x, y) = currentPixel();
    }
    void setPixelVal(unsigned int x, unsigned int y, const pixel& p)
    {
    	getPixel(x, y) = p;
    }
	void line();
    void fill(unsigned int x, unsigned int y, const pixel& oldp, const pixel& newp);
    void tryfill();
    void addBitmap();
    void compose();
    void clip();
	void mark();
	void buildstep(std::string rna);
	void buildsteps(const std::vector<std::string>& rna);
	pixelbuffer getImage() const;
};

#endif /*RNA2FUUN_HPP_*/
